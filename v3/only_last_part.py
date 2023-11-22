import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException
)
import re
import time
import random
from helper_functions import simulate_typing
from selenium import webdriver

def more_button(wait, pattern):
    link = ""
    try:
        more_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "org-overflow-menu__dropdown-trigger")))
        more_button.click()
        more_parents = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "artdeco-dropdown--placement-bottom")))
    except TimeoutException:
        return link
    for parent in more_parents:
        if "more" in parent.text.lower().strip():
            more_parent = parent
    parent_a_tags = more_parent.find_elements(By.TAG_NAME, "a")
    for parent_a_tag in parent_a_tags:
        print(parent_a_tag.text)
        try:
            href = parent_a_tag.get_attribute("href")
            if "linkedin" in href:
                continue
            print("href finded ", href)
        except:
            continue
        link = re.search(pattern, href).group(2)
        print("LINK", link)

    return link

def final_part(driver, wait, pattern, input_filename):
    print("START FINAL PART")
    df = pd.read_csv(input_filename)
    for index, row in df.iterrows():
        original_linkedin_url = "Not Found"
        if pd.isna(row['domain']):
            link = False
            driver.get(row['linkedinUrl'])
            n = 0
            unavailable = False

            while True:
                if n == 2:
                    unavailable = True
                    break

                if "unavailable" in driver.current_url:
                    driver.back()
                    time.sleep(3)
                    driver.forward()
                    time.sleep(3)
                    n += 1
                else:
                    break
                n += 1
            if unavailable:
                continue
            time.sleep(3)

            try:
                btns = wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "org-top-card-primary-actions__action")
                    )
                )
            except TimeoutException:
                btns = []
            if len(btns) >= 1:
                for btn in btns:
                    if btn.get_attribute("tabindex") == "0":
                        link = re.search(pattern, btn.get_attribute("href")).group(2)
            if not link:
                link = more_button(wait, pattern)

            if link:
                df.at[index, "linkedinUrl"] = original_linkedin_url
                df.at[index, "domain"] = link.split("/")[0]
                df.to_csv(input_filename, index=False)
            else:
                print("Continue")
                continue
        else:
            original_linkedin_url = row['linkedinUrl']
    df.drop_duplicates()
    return True

#
def login(driver, action, username, password):
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    time.sleep(5)
    username_inp = driver.find_element(By.ID, "username")
    password_inp = driver.find_element(By.ID, "password")
    action.move_to_element(username_inp).click()
    action.perform()

    simulate_typing(username_inp,username)

    time.sleep(random.uniform(1, 2))
    action.move_to_element(password_inp).click()
    action.perform()

    simulate_typing(password_inp, password)
    button = driver.find_element(
        By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'
    )
    action.move_to_element(button).click()
    action.perform()
    time.sleep(10)


def main(input_filename, username, password):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = uc.Chrome(driver_executable_path="./driver/chromedriver", options=chrome_options)
    wait = WebDriverWait(driver, 60)
    action = webdriver.ActionChains(driver)
    login(driver, action, username, password)
    time.sleep(10)
    final_part(driver, wait, r"https?://(www\.)?([^/]+)", input_filename)

# #s
# if __name__ == "__main__":
#     main("data/output/ruben21294@gmail.com_outdata.csv", "martin.vardanyan.1996@gmail.com", "Dfpotre777")