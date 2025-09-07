# Job Search RPA Tool

Automates scraping job listings from a configurable job portal, enriches company data via an external API, and writes results to a Google Sheet.

#### Prerequisites
- Python 3.10+
- Google service account JSON for Sheets API (set path in SERVICE_ACCOUNT_FILE environment variable or config.py)
- Chrome browser installed
- Optional: CLEARBIT_API_KEY (or other API keys) for company enrichment

#### Setup
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```cmd
   python -m pip install -r requirements.txt
   ```

#### Quick start
1. Put your Google service account JSON file somewhere and set its path:
   ```sh
   export SERVICE_ACCOUNT_FILE="/path/to/service-account.json"
   ```
   on Windows PowerShell:
   ```sh
   $env:SERVICE_ACCOUNT_FILE="C:\path\to\service-account.json"
   ```

3. Configure selectors in `config.py` for your target job portal, or use defaults for a generic portal.

4. Run the tool:
   ```cmd
   python main.py
   ```

#### When prompted, enter:
- Job search query (e.g., "software engineer")
- Number of pages to scrape (e.g., 3)
- Login username (press Enter to skip)
- Login password (press Enter to skip)

#### The script will:
- Launch Chrome (headless by default)
- Log in if credentials are provided
- Scrape job listings using configured selectors
- Enrich company info if a CLEARBIT_API_KEY is set
- Append results into the configured Google Sheet

#### ⚠️ Notes
- This project provides a generic, configurable scraper. You are responsible for complying with the job portal's Terms of Service.
- Update the selectors in `config.py` to match the portal you target.
