import PyInstaller.__main__
import os
from app.metadata import NAME, VERSION


def remove_file(f: str) -> None:
    try:
        os.remove(f)
    except Exception:
        pass


def remove_dir(d: str) -> None:
    try:
        os.rmdir(d)
    except Exception:
        pass


output_filename = f"{NAME}_{VERSION}.exe"
tmp_out_filename = "out.exe"


remove_file(tmp_out_filename)
remove_file(output_filename)

PyInstaller.__main__.run(["main.py", "--onefile", "--console", "--clean", "-n", tmp_out_filename])

remove_file(f"{tmp_out_filename}.spec")
remove_dir("build")

os.rename(f"dist/{tmp_out_filename}", f"dist/{output_filename}")
