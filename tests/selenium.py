import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class weather_webapp_test(unittest.TestCase):
    """ Tests running on weather web app """
    def setUp(self):
        "" Set up the Selenium WebDriver before each test """
        opt = webdriver.ChromeOptions()
        opt.add_argument('ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=opt)
        self.driver.implicitly_wait(0.5)
        self.driver.get("https://10.1.0.8:9090")

    def test_positive_location_response(self):
        """ Test valid location response """
        driver = self.driver
        elem_src = driver.find_element(By.NAME, "location")
        elem_src.send_keys("Denver")
        elem_btn = driver.find_element(By.TAG_NAME, "input")
        elem_btn.submit()
        elem_title = driver.find_elements(By.TAG_NAME, "h2")
        self.assertIn("Forecast", elem_title[0].text)

    def test_negative_location_response(self):
        """ Test invalid location response """
        driver = self.driver
        elem_btn = driver.find_element(By.NAME, "location")
        elem_btn.send_keys("InvalidLocation")
        submit_btn = driver.find_element(By.TAG_NAME, "input")
        submit_btn.submit()
        elem_err_msg = driver.find_elements(By.ID, "err-msg")
        self.assertIn("Location not found", elem_err_msg[0].text)

    def tearDown(self):
        """ Clean up after each test """
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
