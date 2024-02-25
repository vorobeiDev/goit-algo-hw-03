import argparse
from pathlib import Path
import shutil


def copy_files_to_dest(src_path, dest_path) -> None:
    if src_path.is_dir():
        for item in src_path.iterdir():
            if item.is_dir():
                copy_files_to_dest(item, dest_path)
            else:
                copy_file(item, dest_path)
    else:
        copy_file(src_path, dest_path)


def copy_file(file_path, dest_path) -> None:
    extension = file_path.suffix[1:]
    if extension == "":
        extension = "no_extension"
    dest_dir = dest_path / extension
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / file_path.name

    try:
        shutil.copy(file_path, dest_file)
    except Exception as e:
        print(f"Не вдалося скопіювати файл {file_path} до {dest_file}: {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Копіює файли з однієї директорії до іншої, сортуючи їх за розширеннями.")
    parser.add_argument("src_path", type=Path, help="Шлях до вихідної директорії.")
    parser.add_argument("dest_path", type=Path, nargs='?', default=Path("dist"), help="Шлях до директорії призначення.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    if not args.src_path.exists():
        print(f"Вихідна директорія {args.src_path} не існує.")
    elif not args.src_path.is_dir():
        print(f"Вказаний шлях {args.src_path} не є директорією.")
    else:
        args.dest_path.mkdir(parents=True, exist_ok=True)
        copy_files_to_dest(args.src_path, args.dest_path)
        print(f"Файли були успішно скопійовані з {args.src_path} до {args.dest_path}.")
