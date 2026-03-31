import csv
from pathlib import Path


def save_to_csv(data: list[dict[str, str]], file_path: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "name",
            "capital",
            "population",
            "area",
            "fetched_at",
        ])

        for item in data:
            writer.writerow([
                item.get("name", ""),
                item.get("capital", ""),
                item.get("population", ""),
                item.get("area", ""),
                item.get("fetched_at", ""),
            ])