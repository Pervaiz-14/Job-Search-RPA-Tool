from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import logging

from config import HEADLESS, IMPLICIT_WAIT


class SeleniumDriver:
    """Encapsulates WebDriver setup and teardown."""

    def __init__(self, headless: bool = HEADLESS):
        self.headless = headless
        self.driver = None

    def start(self):
        """Start Chrome WebDriver using webdriver-manager for portability."""
        logging.info("Starting Chrome WebDriver (headless=%s)...", self.headless)
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        caps = DesiredCapabilities().CHROME
        caps["goog:loggingPrefs"] = {"browser": "ALL"}

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options, desired_capabilities=caps)
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        return self.driver

    def quit(self):
        """Quit the driver safely."""
        if self.driver:
            try:
                logging.info("Quitting Chrome WebDriver...")
                self.driver.quit()
            except Exception as exc:  # pragma: no cover - defensive
                logging.exception("Error quitting driver: %s", exc)
