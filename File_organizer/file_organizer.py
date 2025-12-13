from pathlib import Path
from pydoc import text

from rich import print
from rich.prompt import Confirm, Prompt


def file_organizer(base_path: str):
    """organize files"""
    file_categories = {
        "Image": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
        "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "Compressed": [".zip", ".rar", ".tar", ".gz", ".7z"],
        "Programs": [".exe", ".msi", ".bat", ".cmd", ".sh", ".bin", ".apk", ".app", ".rpm"],
    }
    base = Path(rf"{base_path}")

    for category, extentions in file_categories.items():
        new_path = base.joinpath(f"{category}")
        existed_before = new_path.exists()
        # create folder (original behavior preserved)
        new_path.mkdir(exist_ok=True, parents=True)
        if existed_before:
            print(f"[dim]Folder already exists:[/dim] [yellow]{new_path}[/yellow]")
        else:
            print(f"[green]Created folder:[/green] [bold]{new_path}[/bold]")

        for ext in extentions:
            for f in base.glob(f"*{ext}"):
                # Print what we are about to do
                print(
                    f"[blue]Processing:[/blue] [white]{f}[/white] -> [cyan]{new_path.name}[/cyan]"
                )
                try:
                    f.move_into(new_path)
                    print(f"[green]Moved:[/green] [bold]{f.name}[/bold] → [cyan]{new_path}[/cyan]")
                except PermissionError:
                    print(f"[red]Permission denied while moving:[/red] [white]{f}[/white]")
                except FileNotFoundError:
                    print(f"[red]File not found (skipped):[/red] [white]{f}[/white]")
                except OSError as e:
                    # handle cases like target is non-empty directory or same path
                    print(f"[red]OS error while moving {f.name}:[/red] {e}")
                except Exception as e:
                    # generic fallback: report error but do not stop the whole run
                    print(f"[red]Failed to move {f.name}:[/red] {e}")


if __name__ == "__main__":
    try:
        my_path = Prompt.ask("[bold blue]Enter your path[/bold blue]", default="~/Downloads")
        file_organizer(base_path=my_path)
        print("[bold green]It's done. All files processed.[/bold green]")
    except Exception as e:
        print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
    finally:
        useful = Confirm.ask("[bold blue]Was this useful?[/bold blue]", default=True)
        if useful:
            print("[bold green]Glad it helped![/bold green]")
        else:
            print("[bold yellow]Thanks for the feedback. I'll improve it.[/bold yellow]")
