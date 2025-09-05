import sys
import logging
from typing import List, Dict

from rpa.selenium_driver import SeleniumDriver
from rpa.scraper import JobScraper
from rpa.company_api import CompanyAPI
from rpa.google_sheets import GoogleSheetsClient
from utils import deduplicate_jobs
import config


def prompt(text: str) -> str:
    print(text, end="", flush=True)
    return sys.stdin.readline().strip()


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def enrich_jobs(jobs: List[Dict], api_client: CompanyAPI) -> List[Dict]:
    out = []
    for job in jobs:
        company = job.get("company")
        enrich = api_client.enrich(company) if company else None
        if enrich:
            job["company_domain"] = enrich.get("domain")
            job["company_logo"] = enrich.get("logo")
            job["company_description"] = enrich.get("description")
            job["company_linkedin"] = enrich.get("linkedin")
        else:
            job.setdefault("company_domain", None)
            job.setdefault("company_logo", None)
            job.setdefault("company_description", None)
            job.setdefault("company_linkedin", None)
        out.append(job)
    return out


def main():
    setup_logging()
    print("Job Search RPA Tool")
    print("-------------------")
    query = prompt("Enter job search query: ")
    pages_in = prompt("Number of pages to scrape (default 1): ")
    try:
        pages = int(pages_in) if pages_in else 1
    except ValueError:
        pages = 1

    username = prompt("Login username (press Enter to skip): ")
    password = prompt("Login password (press Enter to skip): ")

    driver_mgr = SeleniumDriver(headless=config.HEADLESS)
    driver = driver_mgr.start()
    scraper = JobScraper(driver)

    try:
        if username and password:
            scraper.login(username, password)

        raw_jobs = scraper.search_and_collect(query=query, pages=pages)
        print(f"Scraped {len(raw_jobs)} raw job listings.")

        jobs = deduplicate_jobs(raw_jobs)

        api_client = CompanyAPI()
        enriched = enrich_jobs(jobs, api_client)

        sheets = GoogleSheetsClient()
        sheets.connect()
        sheets.append_jobs(enriched)

        print(f"Saved {len(enriched)} jobs to Google Sheet: {config.SHEET_NAME} -> {config.WORKSHEET_NAME}")
    finally:
        driver_mgr.quit()


if __name__ == "__main__":
    main()
