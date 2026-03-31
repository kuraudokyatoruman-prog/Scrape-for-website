import logging
from scraper import fetch_countries
from save_csv import save_to_csv
from save_json import save_to_json


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


def main() -> None:
    url = "https://www.scrapethissite.com/pages/simple/"
    countries = fetch_countries(url)

    if not countries:
        logging.warning("国データを取得できませんでした")
        return

    logging.info(f"{len(countries)} 件の国データを取得しました")

    save_to_csv(countries, "data/countries.csv")
    logging.info("CSV保存完了")

    save_to_json(countries, "data/countries.json")
    logging.info("JSON保存完了")


if __name__ == "__main__":
    main()