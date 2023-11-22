import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class CONTACT_FINDER:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        self.pattern = r"https?://(www\.)?([^/]+)"

    def get_country(self):
        els = self.driver.find_elements(
            By.CLASS_NAME, "text-body-small"
        )
        for el in els:
            if el.tag_name == "span":
                if el.get_attribute("class") == "text-body-small inline t-black--light break-words":
                    return el.text
        return "Not Found"

    def get_company_domains(self, company_name):
        vol_coord = -1
        urls = []
        jobs = self.driver.find_elements(
            By.CLASS_NAME, "pvs-list__item--no-padding-in-columns"
        )
        word = "Present"

        try:
            vol = self.driver.find_element(
                By.XPATH, "//*[contains(text(), 'Volunteering')]"
            )
            vol_coord = vol.location["y"]

        except:
            pass
        for job in jobs:
            if job.location["y"] < vol_coord or vol_coord == -1:
                try:
                    img = job.find_element(By.TAG_NAME, "img")
                    alt_attribute = img.get_attribute("alt")
                    company_name_from_image =  alt_attribute.replace("logo", "").lower().strip()
                    if company_name.lower() == company_name_from_image:
                        continue
                except:
                    print("Bla bla")
                if "Present" in job.text:
                    if job.text[job.text.find(word) + len(word)] == " ":
                        try:
                            a_hrefs = job.find_elements(By.TAG_NAME, "a")

                            if "company" in a_hrefs[0].get_attribute("href"):
                                urls.append(a_hrefs[0].get_attribute("href"))
                        except:
                            pass

        return urls

    #
    def get_email_domain(self, profile_url, true_domain):
        email = "Not Found"
        self.driver.get(
            f"{self.driver.current_url.split('?')[0]}/overlay/contact-info/"
        )
        time.sleep(5)
        try:
            contacts = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "pv-contact-info__contact-type")
                )
            )
        except:
            contacts = []

        for contact in contacts:
            if "Email" in contact.text:
                email = contact.text.split("\n")[1]
                break
        time.sleep(3)
        return email
