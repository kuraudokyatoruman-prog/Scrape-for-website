# 📚 Books Scraper (Python)

## 📝 Overview
This project is a web scraping tool that extracts book data from **Books to Scrape**, a practice website for scraping.

It collects data from both listing pages and detail pages, and saves the results in CSV and JSON formats.

---

## 🚀 Features

- Scrape book data from multiple pages (pagination support)
- Extract detailed information from each product page
- Remove duplicate records
- Save data in CSV and JSON formats
- Separate successful and failed data
- Log failed URLs for retry or debugging

---

## 📊 Extracted Data

Each book contains the following fields:

- `title` – Book title  
- `detail_url` – URL of the detail page  
- `price` – Price of the book  
- `stock` – Availability status  
- `rating` – Rating (One to Five)  
- `upc` – Unique product code  
- `description` – Book description  
- `category` – Book category  
- `fetched_at` – Timestamp of scraping  
- `source_url` – Source listing page URL  

---

## 🧱 Project Structure
<pre>
project
├── main.py
├── scraper.py
├── save_csv.py
├── save_json.py
├── save_failed_csv.py
└── data/
</pre>
---

## ⚙️ Installation
pip install requests beautifulsoup4

---

## ▶️ Usage
python main.py

---

## 📁 Output Files

- `data/books_success.csv`
- `data/books_success.json`
- `data/books_failed.csv`

---

## 💡 Key Design Points

- Separation of concerns:
  - Listing page scraping
  - Detail page scraping
  - Data saving
- Efficient scraping:
  - Duplicate removal to avoid redundant requests
- Robust error handling:
  - Failed requests are logged and saved separately
- Extensible structure:
  - Easy to adapt for other websites

---

## 🔧 Future Improvements

- Parallel processing for faster scraping
- Database integration (SQLite / PostgreSQL)
- Support for additional websites
- CLI arguments for page range control
