# 📚 Books Scraper (Python)

## 📝 Overview
This project is a web scraping tool that extracts country data from **Scrape This Site**, a practice website designed for web scraping.

It collects structured data from a table-based listing page and saves the results in CSV and JSON formats.

---

## 🚀 Features

- Scrape country data from a structured HTML table
- Extract multiple fields from each row
- Save data in CSV and JSON formats
- Clean and simple scraper design
- Easy to extend for other table-based websites

---

## 📊 Extracted Data

Each country contains the following fields:

- `name` – Country name  
- `capital` – Capital city  
- `population` – Population  
- `area` – Area size  
- `fetched_at` – Timestamp of scraping  

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

- `data/countries.csv`
- `data/countries.json`

---

## 💡 Key Design Points

- Separation of concerns:
  - Scraping logic is separated from execution logic
- Structured data extraction:
  - Uses CSS selectors to extract table-based data
- Reusable architecture:
  - Save functions are shared with other projects
- Clean data handling:
  - Handles missing values safely

---

## 🔧 Future Improvements

- Add pagination support (if applicable)
- Convert numeric fields (population, area) to integers
- Add sorting and filtering options
- Store data in a database (SQLite / PostgreSQL)
- Add CLI arguments for flexible execution
