import json
from pathlib import Path


def save_books_to_json(books: list[dict[str, str]], file_path: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
