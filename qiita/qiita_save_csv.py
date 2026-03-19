import csv
from pathlib import Path


def save_articles_to_csv(articles: list[dict[str, str]], file_path: str) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "url", "published_at", "fetched_at"])

        for article in articles:
            writer.writerow(
                [
                    article.get("title", ""),
                    article.get("url", ""),
                    article.get("published_at", ""),
                    article.get("fetched_at", ""),
                ]
            )
