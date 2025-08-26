import torch
import torch.nn as nn
from rich.console import Console
from rich.table import Table
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from inferra.src.utils.inferra_utils import print_msg

console = Console()


class TorchModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.best_state_dict = None

    def summary(self):
        """
        Print a summary of the model
        """
        input_size = getattr(self, "input_size", None)
        if input_size is None:
            input_size = (None,) * 4  # (B, C, H, W)
            print_msg(
                "Warning: Summary may fail if self.input_size isn’t "
                "set while using input_size in your model."
            )

        table = Table(title="Model Summary", show_lines=True)
        table.add_column("Index", style="cyan", justify="center")
        table.add_column("Layer (type)", style="magenta")
        table.add_column("Output Shape", style="green")
        table.add_column("Param #", style="yellow", justify="right")

        hooks = []
        layer_idx = 0
        total_params = 0
        trainable_params = 0

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        dummy_input_size = tuple(1 if x is None else x for x in input_size)
        dummy_input = torch.zeros(dummy_input_size).to(device)
        self.to(device)

        table.add_row("0", "Input Layer", str(list(input_size)), "0")

        def hook_fn(module, input, output):
            nonlocal layer_idx, total_params, trainable_params
            layer_idx += 1
            class_name = module.__class__.__name__
            output_shape = (
                list(output.size())
                if isinstance(output, torch.Tensor)
                else str(output)
            )
            params = sum(p.numel() for p in module.parameters())
            trainable = sum(
                p.numel() for p in module.parameters() if p.requires_grad
            )
            total_params += params
            trainable_params += trainable
            table.add_row(
                str(layer_idx), class_name, str(output_shape), f"{params:,}"
            )

        for module in self.modules():
            if (
                not isinstance(module, (nn.Sequential, nn.ModuleList))
                and module != self
            ):
                hooks.append(module.register_forward_hook(hook_fn))

        self.eval()
        try:
            with torch.no_grad():
                self(dummy_input)
        except RuntimeError:
            raise RuntimeError(
                "Summary failed: input_size used without setting "
                "self.input_size. Please define it in your model "
                "and try again."
            )

        for h in hooks:
            h.remove()

        console.print(table)

        non_trainable_params = total_params - trainable_params
        console.print(
            f"[bold green]Total params:[/bold green] {total_params:,}"
        )
        console.print(
            f"[bold cyan]Trainable params:[/bold cyan] {trainable_params:,}"
        )
        console.print(
            "[bold yellow]Non-trainable params:[/bold yellow] "
            f"{non_trainable_params:,}"
        )
        console.print(f"[bold magenta]Device:[/bold magenta] {device}")

        return {
            "total_params": total_params,
            "trainable_params": trainable_params,
            "non_trainable_params": non_trainable_params,
            "device": str(device),
        }

    def fit(
        self,
        epochs: int,
        optimizer: torch.optim.Optimizer,
        criterion: torch.nn.Module,
        train_dataloader,
        val_dataloader=None,
        scheduler=None,
    ):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = self.to(device)

        if scheduler is None:
            scheduler = torch.optim.lr_scheduler.OneCycleLR(
                optimizer,
                max_lr=0.002,
                epochs=epochs,
                steps_per_epoch=len(train_dataloader),
                pct_start=0.1,
            )

        best_acc = 0.0
        writer = SummaryWriter(getattr(self, "log_dir", "./runs"))

        history = {"train_loss": [], "val_loss": [], "val_acc": []}

        for epoch in range(epochs):
            model.train()
            epoch_loss = 0.0
            progress_bar = tqdm(
                train_dataloader, desc=f"Epoch {epoch + 1}/{epochs}"
            )

            for data, target in progress_bar:
                data, target = data.to(device), target.to(device)
                output = model(data)
                loss = criterion(output, target)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                scheduler.step()

                epoch_loss += loss.item()
                progress_bar.set_postfix({"Loss": f"{loss.item():.4f}"})

            avg_epoch_loss = epoch_loss / len(train_dataloader)
            writer.add_scalar("Loss/Train", avg_epoch_loss, epoch)
            history["train_loss"].append(avg_epoch_loss)

            if val_dataloader is not None:
                model.eval()
                correct, total = 0, 0
                val_loss = 0.0
                with torch.no_grad():
                    for data, target in val_dataloader:
                        data, target = data.to(device), target.to(device)
                        output = model(data)
                        val_loss += criterion(output, target).item()
                        _, predicted = torch.max(output.data, 1)
                        total += target.size(0)
                        correct += (predicted == target).sum().item()

                acc = 100 * correct / total if total > 0 else 0
                avg_val_loss = (
                    val_loss / len(val_dataloader)
                    if len(val_dataloader) > 0
                    else 0
                )

                writer.add_scalar("Loss/Validation", avg_val_loss, epoch)
                writer.add_scalar("Accuracy/Validation", acc, epoch)

                history["val_loss"].append(avg_val_loss)
                history["val_acc"].append(acc)

                print_msg(
                    f"Epoch {epoch + 1} Loss: {avg_epoch_loss:.4f}, "
                    f"Val Loss: {avg_val_loss:.4f}, Accuracy: {acc:.2f}%"
                )

                if acc > best_acc:
                    best_acc = acc
                    self.best_state_dict = model.state_dict()
                    print_msg(f"Best new accuracy: {best_acc:.2f}%")
            else:
                print_msg(
                    f"Epoch {epoch + 1} Loss: {avg_epoch_loss:.4f} "
                    "(no validation data provided)"
                )

        return history

    def load_weights(self, path=None):
        if self.best_state_dict is not None:
            self.load_state_dict(self.best_state_dict)
            print_msg("Loaded model weights.")
        elif path is not None:
            self.load_state_dict(torch.load(path))
        else:
            print_msg(
                "No weights found. Train the model first.", level="warning"
            )

    def forward(self, x):
        raise NotImplementedError(
            "This method is not implemented for this model."
        )
