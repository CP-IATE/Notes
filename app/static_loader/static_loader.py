from pathlib import Path

def get_static_files (filename):
    file_path = Path(__file__).parent.parent / "static" / filename

    with open(file_path, "r") as file:
        return file.read()