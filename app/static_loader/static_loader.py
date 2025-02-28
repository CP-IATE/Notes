from pathlib import Path
from app.static_loader.count_directory import count_directory

def get_static_files (filename):

    steps = count_directory("app")

    steps = int(steps) - 1

    file_path = Path(__file__).parents[steps] / "static" / filename

    with open(file_path, "r") as file:
        return file.read()