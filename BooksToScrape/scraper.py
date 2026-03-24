import requests
import certifi
import logging
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_books(url: str) -> list[dict[str, str]]:
    try:
        response = requests.get(
            url,
            timeout=10,
            verify=certifi.where(),
            headers=HEADERS
        )
        response.raise_for_status()
        time.sleep(random.uniform(1, 2))

    except requests.exceptions.RequestException as e:
        logging.error(f"一覧取得失敗: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for product in soup.select("article.product_pod"):
        title_tag = product.select_one("h3 a")
        price_tag = product.select_one("p.price_color")
        stock_tag = product.select_one("p.instock.availability")
        rating_tag = product.select_one("p.star-rating")

        if not title_tag:
            continue

        title = title_tag.get("title", "").strip()
        link = title_tag.get("href", "").strip()
        detail_url = urljoin(url, link)

        price = price_tag.get_text(strip=True) if price_tag else ""
        stock = stock_tag.get_text(strip=True) if stock_tag else ""

        rating = ""
        if rating_tag:
            classes = rating_tag.get("class", [])
            if len(classes) >= 2:
                rating = classes[1]

        books.append({
            "title": title,
            "detail_url": detail_url,
            "price": price,
            "stock": stock,
            "rating": rating,
        })

    logging.info(f"{len(books)} 件取得: {url}")
    return books


def fetch_book_detail(detail_url: str) -> dict[str, str]:
    try:
        response = requests.get(
            detail_url,
            timeout=10,
            verify=certifi.where(),
            headers=HEADERS
        )
        response.raise_for_status()
        time.sleep(random.uniform(1, 2))

    except requests.exceptions.RequestException as e:
        logging.error(f"詳細取得失敗: {detail_url} - {e}")
        return {
            "upc": "",
            "description": "",
            "category": "",
        }

    soup = BeautifulSoup(response.text, "html.parser")

    upc = ""
    description = ""
    category = ""

    # UPC
    rows = soup.select("table.table.table-striped tr")
    for row in rows:
        th = row.select_one("th")
        td = row.select_one("td")
        if not th or not td:
            continue

        key = th.get_text(strip=True)
        value = td.get_text(strip=True)

        if key == "UPC":
            upc = value

    # 商品説明
    description_tag = soup.select_one("#product_description + p")
    if description_tag:
        description = description_tag.get_text(strip=True)

    # カテゴリ
    breadcrumb_links = soup.select("ul.breadcrumb li a")
    if len(breadcrumb_links) >= 3:
        category = breadcrumb_links[2].get_text(strip=True)

    return {
        "upc": upc,
        "description": description,
        "category": category,
    }
    
def get_next_page_url(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            timeout=10,
            verify=certifi.where(),
            headers=HEADERS
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        logging.error(f"次ページ取得失敗: {url} - {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    next_tag = soup.select_one("li.next a")

    if not next_tag:
        return None

    next_href = next_tag.get("href")
    if not next_href:
        return None

    return urljoin(url, next_href)

def fetch_multiple_book_pages(start_url: str, max_pages: int = 3) -> list[dict[str, str]]:
    all_books = []
    current_url = start_url
    page_count = 0

    while current_url and page_count < max_pages:
        logging.info(f"{page_count + 1}ページ目取得中: {current_url}")

        books = fetch_books(current_url)
        all_books.extend(books)

        current_url = get_next_page_url(current_url)
        page_count += 1

    logging.info(f"合計 {len(all_books)} 件取得しました")
    return all_books

def remove_duplicate_books(books: list[dict[str, str]]) -> list[dict[str, str]]:
    unique_books = []
    seen_urls = set()

    for book in books:
        detail_url = book.get("detail_url", "").strip()

        if not detail_url:
            continue

        if detail_url in seen_urls:
            logging.info(f"重複をスキップ: {detail_url}")
            continue

        seen_urls.add(detail_url)
        unique_books.append(book)

    logging.info(f"重複除去後: {len(unique_books)} 件")
    return unique_books