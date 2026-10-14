"""Real Chrome tests; starts its own local server. Run with unittest discovery."""
import functools
import os
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import threading
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

ROOT = Path(__file__).resolve().parents[1]

class CounterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("mobileEmulation", {"deviceMetrics": {"width": 390, "height": 844, "pixelRatio": 1}})
        if os.environ.get("CHROME_BINARY"):
            options.binary_location = os.environ["CHROME_BINARY"]
        service = Service(os.environ["CHROMEDRIVER"]) if os.environ.get("CHROMEDRIVER") else Service()
        cls.driver = webdriver.Chrome(options=options, service=service)
        cls.addClassCleanup(cls.driver.quit)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(SimpleHTTPRequestHandler, directory=str(ROOT)))
        cls.addClassCleanup(cls.server.server_close)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.addClassCleanup(cls.server.shutdown)
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    def click(self, id):
        self.driver.find_element(By.ID, id).click()

    def value(self):
        return self.driver.find_element(By.ID, "value").text

    def test_numeric(self):
        self.driver.get(self.url)
        self.click("numeric")
        self.assertEqual(self.value(), "0")
        self.assertFalse(self.driver.find_element(By.ID, "minus").is_enabled())
        self.click("plus")
        self.click("plus")
        self.assertEqual(self.value(), "2")
        self.click("minus")
        self.assertEqual(self.value(), "1")
        self.click("reset")
        self.assertEqual(self.value(), "0")

    def test_alphabet(self):
        self.driver.get(self.url)
        self.click("alphabet")
        self.assertEqual(self.value(), "A")
        self.assertFalse(self.driver.find_element(By.ID, "minus").is_enabled())
        for code in range(66, 91):
            self.click("plus")
            self.assertEqual(self.value(), chr(code))
        self.assertFalse(self.driver.find_element(By.ID, "plus").is_enabled())
        self.click("minus")
        self.assertEqual(self.value(), "Y")
        self.click("reset")
        self.assertEqual(self.value(), "A")

    def test_mobile_layout_and_home(self):
        for page in ("index.html", "numeric.html", "alphabet.html"):
            self.driver.get(f"{self.url}/{page}")
            self.assertTrue(self.driver.execute_script("return document.documentElement.scrollWidth <= window.innerWidth"))
            for button in self.driver.find_elements(By.TAG_NAME, "button"):
                self.assertGreaterEqual(button.size["height"], 44)
            if page != "index.html":
                self.driver.find_element(By.CLASS_NAME, "back").click()
                self.assertTrue(self.driver.find_element(By.ID, "numeric").is_displayed())

if __name__ == "__main__":
    unittest.main()
