import logging

from qiita_save_csv import save_articles_to_csv
from qiita_scraper import fetch_multiple_pages, remove_duplicate_articles


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main() -> None:
    start_url = "https://qiita.com/"
    articles = fetch_multiple_pages(start_url, start_page=1, end_page=3)

    if not articles:
        logging.warning("記事を取得できませんでした")
        return

    logging.info("重複除去前: %d 件", len(articles))
    articles = remove_duplicate_articles(articles)

    output_path = "data/qiita_articles.csv"
    save_articles_to_csv(articles, output_path)
    logging.info("CSV保存完了: %s", output_path)


if __name__ == "__main__":
    main()
