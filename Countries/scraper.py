import requests
import certifi
import logging
import time
import random
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_countries(url: str) -> list[dict[str, str]]:
    try:
        response = requests.get(
            url,
            timeout=10,
            verify=certifi.where(),
            headers=HEADERS
        )
        response.raise_for_status()
        time.sleep(random.uniform(1, 2))

    except requests.exceptions.Timeout:
        logging.error("タイムアウトしました")
        return []

    except requests.exceptions.SSLError:
        logging.error("SSL証明書エラー")
        return []

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTPエラー: {e}")
        return []

    except requests.exceptions.RequestException as e:
        logging.error(f"通信エラー: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    countries = []
    fetched_at = datetime.now().isoformat()

    for row in soup.select(".country"):
        name_tag = row.select_one(".country-name")
        capital_tag = row.select_one(".country-capital")
        population_tag = row.select_one(".country-population")
        area_tag = row.select_one(".country-area")

        countries.append({
            "name": name_tag.get_text(strip=True) if name_tag else "",
            "capital": capital_tag.get_text(strip=True) if capital_tag else "",
            "population": population_tag.get_text(strip=True) if population_tag else "",
            "area": area_tag.get_text(strip=True) if area_tag else "",
            "fetched_at": fetched_at,
        })

    logging.info(f"{len(countries)} 件の国データを取得: {url}")
    return countries