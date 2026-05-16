# Wuzzuf Job Scraper

A Python web scraper that collects job listings from [Wuzzuf](https://wuzzuf.net) — Egypt's leading job platform — and exports the data to an Excel file for analysis.

---

## Overview

This project scrapes job postings from Wuzzuf based on a search query (e.g., "Data Analyst" in Egypt), collecting both summary info and full job details across multiple pages. The scraped data is saved as a structured `.xlsx` file.

---

## Dependencies

Install required libraries using pip:

```bash
pip install requests beautifulsoup4 lxml pandas
```

| Library         | Purpose                              |
|----------------|--------------------------------------|
| `requests`      | Sending HTTP requests to Wuzzuf      |
| `beautifulsoup4`| Parsing HTML content                 |
| `lxml`          | HTML parser backend for BeautifulSoup|
| `pandas`        | Data manipulation and Excel export   |

---

## How to Run

```bash
python Script_2.py
```

The script targets this default search URL:

```
https://wuzzuf.net/search/jobs?q=data%20analyst&a=navbg&filters[country][0]=Egypt
```

You can change the search query by modifying the URL passed to `main()` at the bottom of the script.

---

## How It Works

The scraper follows this pipeline:

```
Search Page → Extract Job Cards → Visit Each Job Page → Extract Details → Save to Excel
```

### Functions Breakdown

| Function | Description |
|---|---|
| `main(link)` | Entry point — fetches a search page and starts the scraping pipeline |
| `job_info(different_jobs)` | Extracts title, company, location, and post date for each job card |
| `details_info(de_link)` | Visits each job's detail page and scrapes description & requirements |
| `get_next_link(page)` | Finds the "Next Page" link for pagination |
| `save_to_excel(all_jobs)` | Saves the collected data as `all_jobs.xlsx` |
| `split_text(text)` | Cleans and formats multi-line text fields |
| `check_len(elements)` | Handles single vs. multiple HTML elements |
| `remove_from_company_name(name)` | Removes hyphens from company names |

### Pagination

The scraper automatically follows pagination and scrapes up to **5 pages** (controlled by the `counter` variable — change `counter < 4` to scrape more or fewer pages).

---

## Output

After running, the script generates:

```
all_jobs.xlsx
```

### Columns

| Column | Description |
|---|---|
| `job_title` | Title of the job posting |
| `company_name` | Name of the hiring company |
| `location` | Job location (city, governorate, country) |
| `time` | Time since the job was posted (e.g., "6 days ago") |
| `job description` | Full job description (cleaned and formatted) |
| `job requirements` | Full requirements section (cleaned and formatted) |

### Sample Data

The included `all_jobs.xlsx` contains real scraped listings including roles such as:
- Data Analyst
- Financial Analyst
- Business Analyst
- Senior Data Engineer
- Business Intelligence Engineer
- Supply Chain Data Analyst

...and more, scraped from Egypt-based job postings on Wuzzuf.

---

## Notes & Limitations

- **HTML structure dependency**: The scraper relies on Wuzzuf's current HTML tags and class attributes. If Wuzzuf updates its frontend, the selectors may break and need updating.
- **Rate limiting**: No delays are added between requests. Consider adding `time.sleep()` between calls to avoid getting blocked.
- **Error handling**: Each function has basic try/except blocks that print errors with line numbers without stopping the full scrape.

---

## Project Structure

```
wuzzuf-scraper/
│
├── Script_2.py        # Main scraper script
├── all_jobs.xlsx      # Output file with scraped job data
└── README.md          # Project documentation
```

---

## Possible Improvements

- Add command-line arguments for search query and page limit
- Add `time.sleep()` between requests to reduce server load
- Store data in a database (e.g., SQLite) instead of Excel
- Add proxy rotation to avoid IP blocking
- Build a simple dashboard to visualize the scraped data

---

## Author

Built as a practical application of the `BeautifulSoup` library for web scraping in Python.
