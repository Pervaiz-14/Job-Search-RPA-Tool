from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from typing import List, Dict, Optional
import logging
import time

from config import JOB_PORTAL


class JobScraper:
    """Scraper that logs in (optional), searches, and extracts job listings."""

    def __init__(self, driver):
        self.driver = driver
        self.selectors = JOB_PORTAL["selectors"]
        self.base_url = JOB_PORTAL["base_url"]
        self.login_conf = JOB_PORTAL.get("login", {})

    def login(self, username: str, password: str) -> bool:
        """Attempt to log in. Return True on success, False otherwise."""
        if not username or not password:
            logging.info("No credentials provided; skipping login.")
            return False

        login_url = JOB_PORTAL.get("login_url")
        if not login_url:
            logging.warning("No login URL configured; cannot log in.")
            return False

        logging.info("Navigating to login URL...")
        try:
            self.driver.get(login_url)
            time.sleep(1)
            if "username" in self.login_conf:
                self.driver.find_element(By.CSS_SELECTOR, self.login_conf["username"]).send_keys(username)
            if "password" in self.login_conf:
                self.driver.find_element(By.CSS_SELECTOR, self.login_conf["password"]).send_keys(password)
            if "submit" in self.login_conf:
                self.driver.find_element(By.CSS_SELECTOR, self.login_conf["submit"]).click()
            time.sleep(2)
            logging.info("Login attempt completed.")
            return True
        except WebDriverException as exc:
            logging.exception("Login failed: %s", exc)
            return False

    def _find_text(self, parent, selector: str) -> Optional[str]:
        try:
            el = parent.find_element(By.CSS_SELECTOR, selector)
            return el.text.strip()
        except NoSuchElementException:
            return None

    def _find_attr(self, parent, selector: str, attr: str) -> Optional[str]:
        try:
            el = parent.find_element(By.CSS_SELECTOR, selector)
            return el.get_attribute(attr)
        except NoSuchElementException:
            return None

    def parse_job_card(self, card) -> Dict[str, Optional[str]]:
        """Extract fields from a job card element."""
        title = self._find_text(card, self.selectors["title"])
        company = self._find_text(card, self.selectors["company"])
        location = self._find_text(card, self.selectors["location"])
        link = self._find_attr(card, self.selectors["link"], "href")
        return {
            "title": title,
            "company": company,
            "location": location,
            "url": link,
        }

    def search_and_collect(self, query: str, pages: int = 1) -> List[Dict]:
        """Search for jobs and collect job listings across pages.

        Supports two types of pagination:
        - 'url' (default): constructs search URL with page parameter
        - 'next_button': clicks next button within the site (selector must be set)
        """
        results = []
        pagination = JOB_PORTAL.get("pagination", "url")
        for page in range(1, pages + 1):
            if pagination == "url":
                url = JOB_PORTAL["search_url"].format(query=query, page=page)
                logging.info("Loading search results page: %s", url)
                self.driver.get(url)
                time.sleep(1)
            else:
                # First page must already be loaded for next-button approach
                if page == 1:
                    url = JOB_PORTAL["search_url"].format(query=query, page=1)
                    self.driver.get(url)
                    time.sleep(1)

            cards = self.driver.find_elements(By.CSS_SELECTOR, self.selectors["job_card"])
            logging.info("Found %s job cards on page %s.", len(cards), page)
            for card in cards:
                try:
                    job = self.parse_job_card(card)
                    results.append(job)
                except Exception:
                    logging.exception("Failed to parse one job card; continuing.")
            # handle next_button style (optional)
            if pagination == "next_button" and page < pages:
                next_selector = JOB_PORTAL.get("next_selector")
                if not next_selector:
                    logging.warning("next_selector not configured; stopping pagination.")
                    break
                try:
                    nxt = self.driver.find_element(By.CSS_SELECTOR, next_selector)
                    nxt.click()
                    time.sleep(1)
                except Exception:
                    logging.exception("Failed to click next button; stopping pagination.")
                    break
        return results
