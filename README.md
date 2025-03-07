# Web Crawler for E-commerce Product Discovery

## Overview
This project is a web crawler designed to discover product URLs from e-commerce websites using **Playwright in Python**. The crawler follows a two-step strategy:
1. **Category Crawling**: First, it identifies category pages (e.g., `/electronics`, `/home-appliances`).
2. **Product Crawling**: Then, it navigates inside these categories to extract product URLs.

The output is a structured JSON file mapping each domain to its discovered product pages.

---

## Features
- **Strategic Crawling**: First collects category links, then fetches product links from them.
- **Scalability**: Can handle multiple domains efficiently.
- **Performance Optimization**: Uses asynchronous execution with Playwright for fast crawling.
- **Filtering Mechanism**: Ensures only valid product URLs are extracted, filtering out irrelevant links.
- **Headless Execution**: Can run without a visible browser for automation.

---

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Playwright

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/web-crawler.git
   cd web-crawler
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```sh
   playwright install
   ```

---

## Usage

### Run the Crawler
```sh
python crawl.py
```

### How It Works
1. The script starts by navigating to the **homepage** of the e-commerce site.
2. It extracts **category URLs** based on a predefined filtering logic.
3. For each category, it discovers and extracts **product URLs**.
4. The final output is stored in a JSON file.

---

## Output Structure
The crawler generates a JSON file (`filtered_buy_links.json`) with the format:
```json
{
  "example.com": {
    "https://www.example.com/category": [
      "https://www.example.com/product/1234",
      "https://www.example.com/product/5678"
    ]
  }
}




