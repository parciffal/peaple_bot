import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from linkedin_scraper import actions
from selenium.webdriver.common.by import By

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--start-maximized")
driver = uc.Chrome(
    driver_executable_path="./driver/chromedriver", options=chrome_options
)
wait = WebDriverWait(driver, 60)

import time
actions.login(driver, "gp4128841@gmail.com", "^0R2m0SP51Sz")
time.sleep(2)
driver.get("https://www.linkedin.com/in/rob-feigenbaum-8693622/")
time.sleep(2)
els = driver.find_elements(By.CLASS_NAME, "text-body-small")
for el in els:
    if el.tag_name == "span":
        if el.get_attribute("class") == "text-body-small inline t-black--light break-words":
            print(el.text)
