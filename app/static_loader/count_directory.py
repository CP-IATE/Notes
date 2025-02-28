from pathlib import Path

def count_directory(target_directory):
    file_path = Path(__file__).resolve()

    print(file_path)

    steps = 0

    while file_path.name != target_directory and file_path != file_path.parent:
        file_path = file_path.parent
        steps += 1

    if file_path == file_path.parent:
        print("Directory not found")

    return steps
