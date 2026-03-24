import logging
from scraper import (
    fetch_multiple_book_pages,
    fetch_book_detail,
    remove_duplicate_books,
)
from save_csv import save_books_to_csv
from save_json import save_books_to_json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def main() -> None:
    start_url = "https://books.toscrape.com/"
    books = fetch_multiple_book_pages(start_url, max_pages=3)

    if not books:
        logging.warning("商品を取得できませんでした")
        return

    logging.info(f"重複除去前: {len(books)} 件")
    books = remove_duplicate_books(books)

    success_count = 0
    failed_count = 0
    failed_urls = []

    for book in books:
        detail = fetch_book_detail(book["detail_url"])
        book.update(detail)

        if book.get("upc") or book.get("description") or book.get("category"):
            success_count += 1
            logging.info(f"詳細取得成功: {book['title']}")
        else:
            failed_count += 1
            failed_urls.append(book["detail_url"])
            logging.warning(f"詳細取得失敗: {book['detail_url']}")

    logging.info(f"成功件数: {success_count}")
    logging.info(f"失敗件数: {failed_count}")

    save_books_to_csv(books, "data/books_multi_page.csv")
    save_books_to_json(books, "data/books_multi_page.json")

    logging.info("CSV保存完了")
    logging.info("JSON保存完了")

    if failed_urls:
        logging.info("失敗URL一覧:")
        for failed_url in failed_urls:
            logging.info(failed_url)


if __name__ == "__main__":
    main()