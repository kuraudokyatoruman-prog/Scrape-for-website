import csv
from pathlib import Path


def save_books_to_csv(books: list[dict[str, str]], file_path: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "title",
            "detail_url",
            "price",
            "stock",
            "rating",
            "upc",
            "description",
            "category",
        ])

        for book in books:
            writer.writerow([
                book.get("title", ""),
                book.get("detail_url", ""),
                book.get("price", ""),
                book.get("stock", ""),
                book.get("rating", ""),
                book.get("upc", ""),
                book.get("description", ""),
                book.get("category", ""),
            ])
