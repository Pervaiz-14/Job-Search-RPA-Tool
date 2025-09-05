import gspread
import logging
from typing import List, Dict
from config import SERVICE_ACCOUNT_FILE, SHEET_NAME, WORKSHEET_NAME, BATCH_WRITE_SIZE


class GoogleSheetsClient:
    """Simple client to write rows to Google Sheets using a service account."""

    def __init__(self, service_account_file: str = SERVICE_ACCOUNT_FILE):
        self.service_account_file = service_account_file
        self.client = None
        self.sheet = None
        self.worksheet = None

    def connect(self):
        logging.info("Connecting to Google Sheets using %s", self.service_account_file)
        self.client = gspread.service_account(filename=self.service_account_file)
        try:
            self.sheet = self.client.open(SHEET_NAME)
        except gspread.SpreadsheetNotFound:
            logging.info("Spreadsheet '%s' not found; creating a new one.", SHEET_NAME)
            self.sheet = self.client.create(SHEET_NAME)
            # Share is intentionally left to the user; service account owns the sheet.
        try:
            self.worksheet = self.sheet.worksheet(WORKSHEET_NAME)
        except gspread.WorksheetNotFound:
            logging.info("Worksheet '%s' not found; creating it.", WORKSHEET_NAME)
            self.worksheet = self.sheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="20")
            self._ensure_headers()

    def _ensure_headers(self):
        headers = [
            "Title",
            "Company",
            "Location",
            "Url",
            "Company Domain",
            "Company Logo",
            "Company Description",
            "Company LinkedIn",
        ]
        existing = self.worksheet.row_values(1)
        if existing != headers:
            logging.info("Writing headers to worksheet.")
            self.worksheet.insert_row(headers, index=1)

    def append_jobs(self, jobs: List[Dict]):
        if not self.worksheet:
            self.connect()
        rows = []
        for job in jobs:
            row = [
                job.get("title") or "",
                job.get("company") or "",
                job.get("location") or "",
                job.get("url") or "",
                job.get("company_domain") or "",
                job.get("company_logo") or "",
                job.get("company_description") or "",
                job.get("company_linkedin") or "",
            ]
            rows.append(row)

        # batch write in chunks
        for i in range(0, len(rows), BATCH_WRITE_SIZE):
            chunk = rows[i : i + BATCH_WRITE_SIZE]
            try:
                self.worksheet.append_rows(chunk, value_input_option="RAW")
                logging.info("Appended %s rows to Google Sheet.", len(chunk))
            except Exception:
                logging.exception("Failed to append rows to Google Sheet.")
