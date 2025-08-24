import argparse
import datetime
import glob
import os
import pathlib
import re
import shutil

package = "inferra"  # your package name
build_directory = "tmp_build_dir"
dist_directory = "dist"
to_copy = ["pyproject.toml", "README.md"]


def export_version_string(version, is_nightly=False, rc_index=None):
    """Export Version and Package Name."""
    if is_nightly:
        date = datetime.datetime.now()
        version += f".dev{date:%Y%m%d%H}"
        pyproj_pth = pathlib.Path("pyproject.toml")
        pyproj_str = pyproj_pth.read_text().replace(
            f'name = "{package}"', f'name = "{package}-nightly"'
        )
        pyproj_pth.write_text(pyproj_str)
    elif rc_index is not None:
        version += "rc" + str(rc_index)

    version_file = os.path.join(package, "src", "version.py")
    if os.path.exists(version_file):
        with open(version_file) as f:
            init_contents = f.read()
        with open(version_file, "w") as f:
            init_contents = re.sub(
                "\n__version__ = .*\n",
                f'\n__version__ = "{version}"\n',
                init_contents,
            )
            f.write(init_contents)


def ignore_files(_, filenames):
    return [f for f in filenames if f.endswith("_test.py")]


def copy_source_to_build_directory(root_path):
    os.chdir(root_path)
    os.mkdir(build_directory)
    shutil.copytree(
        package, os.path.join(build_directory, package), ignore=ignore_files
    )
    for fname in to_copy:
        shutil.copy(fname, os.path.join(f"{build_directory}", fname))
    os.chdir(build_directory)


def build(root_path, is_nightly=False, rc_index=None):
    if os.path.exists(build_directory):
        raise ValueError(f"Directory already exists: {build_directory}")

    try:
        copy_source_to_build_directory(root_path)

        from inferra.src.version import __version__

        export_version_string(__version__, is_nightly, rc_index)
        return build_and_save_output(root_path, __version__)
    finally:
        shutil.rmtree(build_directory)


def build_and_save_output(root_path, __version__):
    os.system("python3 -m build")
    os.chdir(root_path)
    if not os.path.exists(dist_directory):
        os.mkdir(dist_directory)
    for fpath in glob.glob(
        os.path.join(build_directory, dist_directory, "*.*")
    ):
        shutil.copy(fpath, dist_directory)

    whl_path = None
    for fname in os.listdir(dist_directory):
        if __version__ in fname and fname.endswith(".whl"):
            whl_path = os.path.abspath(os.path.join(dist_directory, fname))
    if whl_path:
        print(f"Build successful. Wheel file available at {whl_path}")
    else:
        print("Build failed.")
    return whl_path


def install_whl(whl_fpath):
    print(f"Installing wheel file: {whl_fpath}")
    os.system(f"pip3 install {whl_fpath} --force-reinstall --no-dependencies")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--nightly", action="store_true")
    parser.add_argument("--rc", type=int)
    args = parser.parse_args()

    root_path = pathlib.Path(__file__).parent.resolve()
    whl_path = build(root_path, args.nightly, args.rc)
    if whl_path and args.install:
        install_whl(whl_path)
