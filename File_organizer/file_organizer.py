from pathlib import Path
from pydoc import text

from rich import print
from rich.prompt import Prompt


def file_organizer(base_path: str):
    """organize files"""
    file_categories = {
        "Image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
        "Document": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Programs": [".exe", ".msi", ".bat", ".cmd", ".sh", ".bin", ".apk", ".app", ".rpm"],
    }
    base = Path(rf"{base_path}")

    for category, extentions in file_categories.items():
        new_path = base.joinpath(f"{category}")
        new_path.mkdir(exist_ok=True, parents=True)
        for ext in extentions:
            for f in base.glob(f"*{ext}"):
                f.move_into(new_path)


if __name__ == "__main__":
    my_path = Prompt.ask("Enter your path")
    file_organizer(base_path=my_path)
    print("its done")
    exit = Confirm.ask("is it useful?")
