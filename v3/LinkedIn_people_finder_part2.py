#
import pandas as pd
import string
from time import sleep
from selenium import webdriver
from linkedin_scraper import actions
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#
from helper_functions import (
    csv_to_dict,
    dict_to_csv,
    remove_old_output
)
#
from rocket_reach import (
    rocket_reach_by_linkedin_url,
    process_data
)

#
from contact_finder import CONTACT_FINDER


#
class LinkedinScraperPart2:
    def __init__(self, username, password, people_to_chep_input_name, first_input, driver):
        self.output_filename = "./data/output/{}_outdata_3.csv".format(username)
        self.LOCAL_DATA_FOLDER = "data/"
        self.first_part_data = csv_to_dict(first_input)
        self.ceo_priority_data = csv_to_dict("data/input/ceo_priority.csv")
        self.marketing_priority_data = csv_to_dict("data/input/marketing_priority.csv")
        self.input_name = people_to_chep_input_name
        self.username = username
        self.password = password
        self.driver = driver
        self.action = webdriver.ActionChains(self.driver)
        self.contact_finder = CONTACT_FINDER(self.driver)
        self.csv_data = csv_to_dict(self.input_name)
        self.wait = WebDriverWait(self.driver, 60)
        self.position_data = self.first_part_data["position_1"].dropna().to_list()
        self.ignore_keywords = [word.lower().strip() for word in self.first_part_data["ignore_keywords"].dropna().to_list()]
        self.filtered_positions = []
        for pos_line in self.position_data:
            self.filtered_positions += [
                pos.strip().lower() for pos in pos_line.split("=")
            ]

    #
    def stnadard_variant(self, j, finded):
        try:
            span = j.find_element(By.TAG_NAME, "span")
        except:
            return ""
        if self.company_title.lower().strip().replace("®", "") == span.text.lower().strip():
            try:
                jobs_div = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "pvs-entity--with-path")
                    )
                )
            except TimeoutException:
                finish_position = span.text
                finded = True
                return finish_position

            job_span = jobs_div.find_element(By.TAG_NAME, "span")

            finish_position = job_span.text
        else:
            finish_position = span.text
            finded = True
        if finded:
            return finish_position
        else:
            return ""

    #
    def image_variant(self, li, j, finish_position):
        img_elements = li.find_elements(By.TAG_NAME, "img")
        for img_element in img_elements:
            alt_attribute = img_element.get_attribute("alt")
            if alt_attribute.replace("logo", "").lower().strip() == self.company_title.lower().strip():
                try:
                    span = j.find_element(By.TAG_NAME, "span")
                except:
                    continue
                if any(
                    word.strip() in self.true_company_title.lower().strip()
                    for word in span.text.split()
                    if len(word.strip()) > 1 and word.strip() not in string.punctuation
                ):
                    try:
                        jobs_div = self.wait.until(
                            EC.presence_of_element_located(
                                (
                                    By.CLASS_NAME,
                                    "pvs-entity--with-path",
                                )
                            )
                        )
                    except TimeoutException:
                        finish_position = span.text
                        return finish_position
                    job_span = jobs_div.find_element(By.TAG_NAME, "span")
                    finish_position = job_span.text
                    return finish_position
                else:
                    finish_position = span.text
                    return finish_position
            else:
                return finish_position
        return finish_position

    #
    def find_true_priority(self, position):
        if 10 <= self.employee_count < 70:
            self.ceo_priority_data['position_lower'] = self.ceo_priority_data['position'].str.lower()
            result_df = self.ceo_priority_data[self.ceo_priority_data['position_lower'] == position.lower()]
            if not result_df.empty:
                return result_df['priority'].values[0]
            else:
                return 5000
        if 70 <= self.employee_count <= 400:
            self.marketing_priority_data['position_lower'] = self.marketing_priority_data['position'].str.lower()
            result_df = self.marketing_priority_data[self.marketing_priority_data['position_lower'] == position.lower()]
            if not result_df.empty:
                return result_df['priority'].values[0]
            else:
                return 5000
        return False

    #
    def scrap_data(self, current_work):
        try:
            sections = self.wait.until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "section"))
            )
        except TimeoutException:
            sleep(5)
            try:
                sections = self.wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "section"))
                )
            except TimeoutException:
                print("We couldn't find section in Profile page")
                return False
        finish_position = ""
        for section in sections:
            finded = False
            try:
                header = section.find_element(By.CLASS_NAME, "pvs-header__container")
            except:
                continue
            header_span = header.find_element(By.TAG_NAME, "span")
            if "experience" not in header_span.text.lower():
                continue
            else:
                print("find experience")
                lis = section.find_elements(By.TAG_NAME, "li")
                for li in lis:
                    jobs = li.find_elements(By.CLASS_NAME, "justify-space-between")
                    for j in jobs:
                        location = j.location["x"]
                        if (
                            self.company_title.lower().strip().replace("®", "") in j.text.lower()
                            and location < 1000
                        ):
                            finish_position = self.stnadard_variant(j, finded)
                            if not finish_position:
                                continue
                        else:
                            finish_position = self.image_variant(li, j, finish_position)
        if " at " in finish_position.lower().strip():
            finish_position = finish_position.split(" at ")[0].lower().strip()
        for _pos in self.filtered_positions:
            if _pos == finish_position.lower().strip():
                current_work = True
                break
        for ignore_word in self.ignore_keywords:
            if ignore_word.lower() in finish_position.lower():
                print("IGNORE WORD EXIST CURRENT WORK SETED FALSE")
                current_work = False

        country = self.contact_finder.get_country()
        true_priority = self.find_true_priority(finish_position)
        if true_priority == 5000:
            return False
        if not true_priority:
            return False

        out_data = {
            "original domain": self.domain,
            "linkedinUrl": self.company_url[:-1] if self.company_url.endswith("/") else self.company_url,
            "fullName": self.full_name,
            "name": self.name,
            "surname": self.surname,
            "url": self.driver.current_url.split("overlay/contact-info/")[0][:-1] if self.driver.current_url.split("overlay/contact-info/")[0].endswith("/") else self.driver.current_url.split("overlay/contact-info/")[0] ,
            "good": current_work,
            "position": finish_position.split("•")[0],
            "keyword": self.keyword,
            "employee count": self.employee_count,
            "company name": self.true_company_title,
            "country": country,
            "email": self.email,
            "priority": true_priority,
            "favorite": self.favorite,
            "fake": "Not Fake",
            "domain": self.domain,
            "variant 1": self.variant_1,
            "variant 2": self.variant_2,
            "variant 3": self.variant_3,
            "variant 4": self.variant_4,
            "variant 5": self.variant_5,
            "variant 6": self.variant_6,
            "variant 7": self.variant_7
        }
        dict_to_csv(out_data, self.username, "3")

    #
    def not_email_from_company(self, group_sorted_first_5):
        i = 0
        data = {}
        for index, row in group_sorted_first_5.iterrows():
            if row['linkedinUrl'] == "Not found":
                return False
            if i == 5:
                break
            self.linkedin_profile_url = row['linkedinUrl']
            self.keyword = row['keyword']
            self.company_title = row['company name']
            self.true_company_title = row['company name']
            self.domain = row['original domain']
            self.company_url = row['url']
            self.full_name = row['fullName']
            self.name = row["name"]
            self.surname = row['surname']
            self.employee_count = row['employee count']
            self.email = row['Variant 1']
            self.variant_1 = row['Variant 2']
            self.variant_2 = row['Variant 3']
            self.variant_3 = row['Variant 4']
            self.variant_4 = row['Variant 5']
            self.variant_5 = row['Variant 6']
            self.variant_6 = row['Variant 7']
            self.variant_7 = row['Variant 8']
            self.driver.get(self.linkedin_profile_url)
            sleep(3)
            current_work = False
            try:
                sections = self.wait.until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "section"))
                )
            except TimeoutException:
                sleep(5)
                try:
                    sections = self.wait.until(
                        EC.presence_of_all_elements_located((By.TAG_NAME, "section"))
                    )
                except TimeoutException:
                    print("We couldn't find section in Profile page")
                    return False
            finish_position = ""
            for section in sections:
                finded = False
                try:
                    header = section.find_element(By.CLASS_NAME, "pvs-header__container")
                except:
                    continue
                header_span = header.find_element(By.TAG_NAME, "span")
                if "experience" not in header_span.text.lower():
                    continue
                else:
                    print("find experience")
                    lis = section.find_elements(By.TAG_NAME, "li")
                    for li in lis:
                        jobs = li.find_elements(By.CLASS_NAME, "justify-space-between")
                        for j in jobs:
                            location = j.location["x"]
                            if (
                                self.company_title.lower().strip().replace("®", "") in j.text.lower()
                                and location < 1000
                            ):
                                finish_position = self.stnadard_variant(j, finded)
                                if not finish_position:
                                    continue
                            else:
                                finish_position = self.image_variant(li, j, finish_position)
            if " at " in finish_position.lower().strip():
                finish_position = finish_position.split(" at ")[0].lower().strip()
            for _pos in self.filtered_positions:
                if _pos == finish_position.lower().strip():
                    current_work = True
                    break
            for ignore_word in self.ignore_keywords:
                if ignore_word.lower() in finish_position.lower():
                    print("IGNORE WORD EXIST CURRENT WORK SETED FALSE")
                    current_work = False

            country = self.contact_finder.get_country()
            true_priority = self.find_true_priority(finish_position)
            if true_priority == 5000:
                continue
            elif not true_priority:
                continue
            else:
                data[index] = [true_priority, current_work, country, self.linkedin_profile_url, self.domain, finish_position]
                i+=1
        sorted_data = dict(sorted(data.items(), key=lambda item: item[1][0]))
        
        for index in sorted_data:
            print("SPRTED DATA", sorted_data[index])
            email = rocket_reach_by_linkedin_url(sorted_data[index][3])
            email = process_data(email, sorted_data[index][4])
            if email:
                out_data = {
                    "original domain": sorted_data[index][4],
                    "linkedinUrl": self.company_url[:-1] if self.company_url.endswith("/") else self.company_url,
                    "fullName": self.full_name,
                    "name": self.name,
                    "surname": self.surname,
                    "url": sorted_data[index][3],
                    "good": sorted_data[index][1],
                    "position": sorted_data[index][5],
                    "keyword": self.keyword,
                    "employee count": self.employee_count,
                    "company name": self.true_company_title,
                    "country": sorted_data[index][2],
                    "email": email,
                    "priority": sorted_data[index][0],
                    "favorite": "Favorite",
                    "fake": "Not Fake",
                    "domain": sorted_data[index][4],
                    "variant 1": self.variant_1,
                    "variant 2": self.variant_2,
                    "variant 3": self.variant_3,
                    "variant 4": self.variant_4,
                    "variant 5": self.variant_5,
                    "variant 6": self.variant_6,
                    "variant 7": self.variant_7
                }
                dict_to_csv(out_data, self.username, "3")
                return True
        return False

    def start(self):
        remove_old_output(self.output_filename)
        grouped = self.csv_data.groupby("company name")
        actions.login(self.driver, self.username, self.password)
        for company, group in grouped:
            print(f"Company: {company}")
            group_sorted_first_5 = group.sort_values(by="priority")
            if all((group['Variant 1'] == '') | (group['Variant 1'].isna()) | (group['priority'] == 5000)):
                self.not_email_from_company(group_sorted_first_5)
            else:
                i = 0
                for index, row in group_sorted_first_5.iterrows():
                    if i == 5:
                        break
                    if not row["Variant 1"]:
                        continue
                    if pd.isna(row["Variant 1"]):
                        continue
                    current_work = False
                    self.favorite = "Not checked"
                    self.keyword = row['keyword']
                    self.linkedin_profile_url = row['linkedinUrl']
                    self.company_title = row['company name']
                    self.true_company_title = row['company name']
                    self.domain = row['original domain']
                    self.company_url = row['url']
                    self.full_name = row['fullName']
                    self.name = row["name"]
                    self.surname = row['surname']
                    self.employee_count = row['employee count']
                    self.email = row['Variant 1']
                    self.variant_1 = row['Variant 2']
                    self.variant_2 = row['Variant 3']
                    self.variant_3 = row['Variant 4']
                    self.variant_4 = row['Variant 5']
                    self.variant_5 = row['Variant 6']
                    self.variant_6 = row['Variant 7']
                    self.variant_7 = row['Variant 8']
                    self.priority = row['priority']
                    self.driver.get(self.linkedin_profile_url)
                    sleep(5)
                    self.scrap_data(current_work)
                    sleep(2)
                    i+=1
        return self.output_filename

    @staticmethod
    def check_output(input_name):
        df = pd.read_csv(input_name)
        min_priority = df.groupby("original domain")['priority'].transform('min')
        df["favorite"] = ["Favorite" if priority == min_val and min_val < 5000 else "Not Favorite" for priority, min_val in zip(df["priority"], min_priority)]
        df.to_csv(input_name, index=False, encoding="utf-8")


# if __name__ == "__main__":
#     bot = LinkedinScraperPart2("martin.vardanyan.1996@gmail.com", "Dfpotre777", "output/output.csv", "input/ruben21294@gmail.com_input.csv")
#     bot.start()