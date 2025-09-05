"""
Configuration for the Job Search RPA Tool.

Adjust selectors to match your target job portal.
Environment variables:
- SERVICE_ACCOUNT_FILE: path to Google service account JSON
- CLEARBIT_API_KEY: optional API key for company enrichment
"""

import os

# Google Sheets
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE", "service-account.json")
SHEET_NAME = os.environ.get("SHEET_NAME", "Job Applications Tracker")
WORKSHEET_NAME = os.environ.get("WORKSHEET_NAME", "Jobs")

# Scraper options
HEADLESS = True  # Set to False to watch the browser
IMPLICIT_WAIT = 8  # seconds

# Default job portal configuration (generic / must be customized)
JOB_PORTAL = {
    "base_url": "https://example-job-portal.local",  # replace with actual portal
    "login_url": "https://example-job-portal.local/login",
    "search_url": "https://example-job-portal.local/search?q={query}&page={page}",
    # CSS selectors for a single job card
    "selectors": {
        "job_card": ".job-card",  # container selector for each job listing
        "title": ".job-title",
        "company": ".company-name",
        "location": ".job-location",
        "link": "a.job-link",  # anchor within job-card; get href
    },
    # Login selectors
    "login": {
        "username": "input[name='username']",
        "password": "input[name='password']",
        "submit": "button[type='submit']",
    },
    # Pagination: if present, how to advance pages; can be 'url' or 'next_button'
    "pagination": "url",
}

# External company enrichment API
CLEARBIT_API_KEY = os.environ.get("CLEARBIT_API_KEY", "")
CLEARBIT_ENDPOINT = "https://company.clearbit.com/v2/companies/find?name={name}"

# Save settings
BATCH_WRITE_SIZE = 50  # write to Google Sheets in batches
