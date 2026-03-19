import logging
import random
import re
import time
from datetime import datetime
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import certifi
import requests
from bs4 import BeautifulSoup, Tag


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")


def build_page_url(base_url: str, page: int) -> str:
    parsed = urlparse(base_url)
    query = dict(parse_qsl(parsed.query))
    query["page"] = str(page)
    new_query = urlencode(query)
    return urlunparse(parsed._replace(query=new_query))


def _extract_title_link(article: Tag, base_url: str) -> tuple[str, str]:
    title_tag = article.select_one("h2 a") or article.select_one("h1 a") or article.select_one("h3 a")

    if title_tag is None:
        return "", ""

    title = title_tag.get_text(strip=True)
    href = title_tag.get("href", "").strip()

    if not title or not href:
        return "", ""

    full_url = urljoin(base_url, href)
    return title, full_url


def _extract_published_at(article: Tag) -> str:
    time_tag = article.find("time")
    if time_tag is not None:
        datetime_value = time_tag.get("datetime")
        if datetime_value:
            return datetime_value.strip()

        visible_text = time_tag.get_text(strip=True)
        if visible_text:
            return visible_text

    text = article.get_text(" ", strip=True)
    match = DATE_PATTERN.search(text)
    return match.group(0) if match else ""


def fetch_articles(url: str) -> list[dict[str, str]]:
    try:
        response = requests.get(
            url,
            timeout=10,
            verify=certifi.where(),
            headers=HEADERS,
        )
        response.raise_for_status()
        time.sleep(random.uniform(1, 2))

    except requests.exceptions.Timeout:
        logging.error("タイムアウトしました: %s", url)
        return []
    except requests.exceptions.SSLError:
        logging.error("SSL証明書エラー: %s", url)
        return []
    except requests.exceptions.HTTPError as e:
        logging.error("HTTPエラー: %s", e)
        return []
    except requests.exceptions.RequestException as e:
        logging.error("通信エラー: %s", e)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    fetched_at = datetime.now().isoformat(timespec="seconds")
    articles: list[dict[str, str]] = []

    for article in soup.find_all("article"):
        title, full_url = _extract_title_link(article, url)
        if not title or not full_url:
            continue

        published_at = _extract_published_at(article)

        articles.append(
            {
                "title": title,
                "url": full_url,
                "published_at": published_at,
                "fetched_at": fetched_at,
            }
        )

    logging.info("%d 件の記事を取得: %s", len(articles), url)
    return articles


def fetch_multiple_pages(base_url: str, start_page: int, end_page: int) -> list[dict[str, str]]:
    all_articles: list[dict[str, str]] = []

    for page in range(start_page, end_page + 1):
        paged_url = build_page_url(base_url, page)
        logging.info("%d ページ目を取得中: %s", page, paged_url)
        articles = fetch_articles(paged_url)
        all_articles.extend(articles)

    return all_articles


def remove_duplicate_articles(articles: list[dict[str, str]]) -> list[dict[str, str]]:
    unique_articles: list[dict[str, str]] = []
    seen_urls: set[str] = set()

    for article in articles:
        url = article["url"]
        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_articles.append(article)

    logging.info("重複除去後: %d 件", len(unique_articles))
    return unique_articles
