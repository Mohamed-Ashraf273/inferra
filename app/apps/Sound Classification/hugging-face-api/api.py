import io

import soundfile as sf
import torch
import torch.nn as nn
import torchaudio.transforms as transforms
from fastapi import FastAPI
from fastapi import UploadFile

from inferra.src.models.au57 import Au57  # your custom class

device = torch.device("cpu")
model = Au57(num_classes=50).to(device)
model.load_state_dict(torch.load("au57_weights.pth", map_location=device))
model.eval()

idx_to_class = {
    0: "airplane ✈️",
    1: "breathing 😮‍💨",
    2: "brushing_teeth 🪥",
    3: "can_opening 🥫",
    4: "car_horn 🚗📢",
    5: "cat 🐱",
    6: "chainsaw 🪚",
    7: "chirping_birds 🐦",
    8: "church_bells 🔔",
    9: "clapping 👏",
    10: "clock_alarm ⏰",
    11: "clock_tick 🕰️",
    12: "coughing 🤧",
    13: "cow 🐄",
    14: "crackling_fire 🔥",
    15: "crickets 🦗",
    16: "crow 🪶",
    17: "crying_baby 👶😭",
    18: "dog 🐶",
    19: "door_wood_creaks 🚪",
    20: "door_wood_knock 🚪🔨",
    21: "drinking_sipping 🥤",
    22: "engine 🏎️",
    23: "fireworks 🎆",
    24: "footsteps 👣",
    25: "frog 🐸",
    26: "glass_breaking 🥂💥",
    27: "hand_saw 🪓",
    28: "helicopter 🚁",
    29: "hen 🐔",
    30: "insects 🐞",
    31: "keyboard_typing ⌨️",
    32: "laughing 😂",
    33: "mouse_click 🖱️",
    34: "pig 🐷",
    35: "pouring_water 💧",
    36: "rain 🌧️",
    37: "rooster 🐓",
    38: "sea_waves 🌊",
    39: "sheep 🐑",
    40: "siren 🚨",
    41: "sneezing 🤧",
    42: "snoring 😴",
    43: "thunderstorm ⛈️",
    44: "toilet_flush 🚽",
    45: "train 🚆",
    46: "vacuum_cleaner 🧹",
    47: "washing_machine 🧺",
    48: "water_drops 💦",
    49: "wind 🌬️",
}

transform = nn.Sequential(
    transforms.MelSpectrogram(
        sample_rate=22050,
        n_fft=1024,
        hop_length=512,
        n_mels=128,
        f_min=0,
        f_max=11025,
    ),
    transforms.AmplitudeToDB(),
)

app = FastAPI(title="Au57 Sound Classifier API")


def preprocess(waveform):
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    spectrogram = transform(waveform)
    return spectrogram.unsqueeze(0).to(device)


@app.post("/predict")
async def predict(file: UploadFile):
    contents = await file.read()
    audio_buffer = io.BytesIO(contents)

    waveform, sr = sf.read(audio_buffer, dtype="float32")
    waveform = torch.tensor(waveform).T  # [channels, samples]

    inputs = preprocess(waveform)

    with torch.no_grad():
        logits = model(inputs)
        probs = torch.softmax(logits, dim=1).cpu().numpy().tolist()
        pred_idx = int(torch.argmax(logits, dim=1).item())
        pred_class = idx_to_class[pred_idx]

    return {"pred_class": pred_class, "pred_vector": probs}
