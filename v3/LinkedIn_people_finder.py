#
import time
import string
import random

#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

#
from helper_functions import (
    simulate_typing,
    get_employee_count,
    check_company_size,
    scroll,
    check_unavailable,
    artdeco_card__with_hover,
    not_found_data,
    csv_to_dict,
    dict_to_csv,
    process_string,
    check_word,
    remove_old_output
)
#from aws_tools import AWSTools


#
class LinkedinScraper:
    #
    def __init__(self, username, password, input_name, driver):
        self.output_filename = "./data/output/{}_outdata_1.csv".format(username)
        self.LOCAL_DATA_FOLDER = "data/"
        self.input_name = input_name
        self.username = username
        self.password = password
        self.linkedin_url = ""
        self.domain = ""
        self.company_title = ""
        self.true_company_title = ""
        self.outdata = []
        self.employee_count = 0
        self.main_url = "https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin"
        self.driver = driver
        #self.aws_client = AWSTools()
        self.action = webdriver.ActionChains(self.driver)
        #self.aws_client.get_input_from_bucket(self.username)
        time.sleep(10)
        self.csv_data = csv_to_dict(input_name)
        self.position_data = self.csv_data["position_1"].dropna().to_list()
        self.ignore_keywords = [word.lower().strip() for word in self.csv_data["ignore_keywords"].dropna().to_list()]
        self.filtered_positions = []
        for pos_line in self.position_data:
            self.filtered_positions += [
                pos.strip().lower() for pos in pos_line.split("=")
            ]

        self.wait = WebDriverWait(self.driver, 60)
        self.unsubscribe = self.csv_data["unsubscribe"].dropna().to_list()
        self.ceo_priority_data = csv_to_dict("./data/input/ceo_priority.csv")
        self.marketing_priority_data = csv_to_dict("./data/input/marketing_priority.csv")

    #
    def login(self):
        self.username_inp = self.driver.find_element(By.ID, "username")
        self.password_inp = self.driver.find_element(By.ID, "password")
        self.action.move_to_element(self.username_inp).click()
        self.action.perform()

        simulate_typing(self.username_inp, self.username)

        time.sleep(random.uniform(1, 2))
        self.action.move_to_element(self.password_inp).click()
        self.action.perform()

        simulate_typing(self.password_inp, self.password)

        self.button = self.driver.find_element(
            By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'
        )
        self.action.move_to_element(self.button).click()
        self.action.perform()
        time.sleep(30)

    #
    def get_peoples_page(self, company):
        self.linkedin_url = company
        self.driver.get(company)
        n = 0
        while True:
            if n == 2:
                return False
            try:
                self.true_company_title = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                ).text
                print("TRUE COMPANY TITLE ", self.true_company_title)
                break
            except TimeoutException:
                print("TIMEOUT EXCEPTION")
                if check_unavailable(self.driver):
                    return False
                self.driver.back()
                time.sleep(3)
                self.driver.forward()
                time.sleep(5)
            n += 1

        if self.true_company_title:
            self.company_title = self.true_company_title.lower().strip()
        time.sleep(2)
        if "about" in self.driver.current_url:
            self.company_name = self.driver.current_url.split("/")[-3]
        else:
            self.company_name = self.driver.current_url.split("/")[-2]
        z = 0
        while True:
            if z == 2:
                return False
            try:
                self.driver.get(
                    "https://www.linkedin.com/company/{}/people/".format(
                        self.company_name
                    )
                )
                break
            except:
                print("WE CAN't GO TO PEOPLE PAGE")
                self.driver.back()
                time.sleep(3)
                self.driver.forward()
                time.sleep(5)
            z += 1
        self.company_people_url = self.driver.current_url
        return True

    #
    def start_empoyee_scan(self):
        line = 0
        self.company_data = self.csv_data["company"].dropna().to_list()
        self.domain_data = self.csv_data["domain"].dropna().to_list()
        while line < len(self.company_data):
            self.finded_people_count = 0
            self.taken_people = []
            time.sleep(2)
            self.domain = self.domain_data[line]
            print("Company is", self.company_data[line])
            people_page = self.get_peoples_page(self.company_data[line])
            if not people_page:
                line += 1
                time.sleep(2)
                continue
            employee_count = get_employee_count(self.driver, self.wait)
            print("EMPLOYEES COUNT", employee_count)
            if not employee_count:
                line += 1
                time.sleep(2)
                continue
            else:
                self.employee_count = employee_count

            if self.employee_count > 400:
                line += 1
                continue
            if self.employee_count < 10:
                line += 1
                continue

            time.sleep(random.uniform(4, 5))
            if not check_company_size(self.employee_count):
                scroll(self.driver, self.wait)
                time.sleep(3)
                self.search_positions(employees_count=self.employee_count)
            else:
                self.search_keywords(self.employee_count)
            line += 1
            time.sleep(2)

    #
    def find_matched_people(self, position, link, full_name):
        try:
            for pos in self.filtered_positions:
                if len(position) > 0:
                    if pos.lower() in position.split(" at ")[0].lower():
                        if link not in self.taken_people:
                            link_for_check = link.split("?")[0] + "/"
                            print("Link for check: ", link_for_check)
                            if link_for_check in self.unsubscribe:
                                print(
                                    "detected unsubscribe link: ",
                                    link_for_check,
                                )
                                continue
                            else:
                                print("POSITION", pos)
                                print("FULL NAME", full_name)
                                names = full_name.split()
                                finish_names = []
                                for name in names:
                                    name = check_word(name)
                                    name = process_string(name)
                                    if name:
                                        finish_names.append(name)
                                self.matched_members.append([position.split(" at ")[0], link, finish_names, full_name])
                                self.taken_people.append(link)
        except Exception as e:
            print("Error:", e)
            return False

    #
    def loop_over_positions(self, link_positions):
        for i in link_positions:
            try:
                link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
            except NoSuchElementException:
                print("NoSuchElementException: can't find", i.text)
                continue
            except:
                print("Excpetion: can't find", i.text)
                continue
            k = 0
            work = False
            while True:
                if k == 2:
                    work = True
                    break
                try:
                    position_element = i.find_element(
                        By.CLASS_NAME,
                        "t-black--light",
                    )
                    position = position_element.text
                    if not position.replace(" ", "").replace("\n", "").replace("\t", ""):
                        position = self.driver.execute_script("return arguments[0].textContent;", position_element).replace("\n", "").replace("\t", "").strip()
                    full_name_element = i.find_element(
                        By.CLASS_NAME, "org-people-profile-card__profile-title"
                    )
                    full_name = full_name_element.text
                    if not full_name.replace(" ", "").replace("\n", "").replace("\t", ""):
                        full_name = self.driver.execute_script("return arguments[0].textContent;", full_name_element).replace("\n", "").replace("\t", "").strip()
                    print("LINK", link)
                    print("POSITION", position)
                    print("FULL NAME",full_name)
                    break
                except:
                    self.driver.back()
                    time.sleep(3)
                    self.driver.forward()
                    time.sleep(5)
                    k+=1
            if work:
                continue
            matched = self.find_matched_people(position, link, full_name)
            if not matched:
                continue

    #
    def stnadard_variant(self, j, finded):
        try:
            span = j.find_element(By.TAG_NAME, "span")
        except:
            return ""
        if self.company_title.replace("®", "") == span.text.lower().strip():
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
        print("IMAGE VARIANT")
        img_elements = li.find_elements(By.TAG_NAME, "img")
        for img_element in img_elements:
            alt_attribute = img_element.get_attribute("alt")
            if alt_attribute.replace("logo", "").lower().strip() == self.company_title:
                try:
                    span = j.find_element(By.TAG_NAME, "span")
                except:
                    continue
                if any(
                    word.strip() in self.true_company_title
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
                        print("SPAN FIN TEXT", finish_position)
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
    def search_positions(self, keyword=False, employees_count=False):
        self.matched_members = []
        link_positions, unavailable = artdeco_card__with_hover(
            self.driver, self.wait, self.employee_count, False
        )
        if unavailable:
            not_found_data(
                self.linkedin_url,
                self.domain,
                self.employee_count,
                self.true_company_title,
                self.username,
            )
            return "UNAVAILABLE"

        self.loop_over_positions(link_positions)

        if len(self.matched_members) == 0:
            print("NOT FINDED MATCHED")
            if keyword == False:
                not_found_data(
                    self.linkedin_url,
                    self.domain,
                    employees_count,
                    self.true_company_title,
                    self.username,
                )
            return "FALSE"
        
        for member_link in self.matched_members:
            position, link, finish_names, full_name = member_link
            print("POSITION 1 ", position)
            print("FINISH NAMES 1 ", finish_names)
            print("FULL NAME 1 ", full_name)
            out_data = {
                "original domain": self.domain,
                "linkedinUrl": link.split("?")[0],
                "fullName": full_name,
                "name": finish_names[0] if len(finish_names) > 0 else " ",
                "surname": finish_names[1] if len(finish_names) > 1 else " ",
                "good": "",
                "url": self.driver.current_url.split("overlay/contact-info/")[0].replace("people/", ""),
                "position": position,
                "keyword": "Not Found",
                "employee count": self.employee_count,
                "company name": self.true_company_title,
                "country": "",
                "email": "",
                "fake": "Not Fake",
                "domain": self.domain,
                "priority": self.add_priority(position)
            }
            if keyword:
                out_data["keyword"] = keyword.lower()
            dict_to_csv(out_data, self.username, "1")

        return False

    #
    def search_keywords(self, employees_count):
        main_finded = False
        unavailable = False
        self.matched_keywords = {}
        self.keyword_data = self.csv_data["keyword_1"].dropna().to_list()

        for n, key in enumerate(self.keyword_data):
            if self.finded_people_count >= 5:
                break
            z = 0
            while True:
                if z == 2:
                    unavailable = True
                    break
                try:
                    search_input = self.wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="people-search-keywords"]')
                        )
                    )
                    break
                except TimeoutException:
                    z += 1
                    if "unavailable" in self.driver.current_url:
                        unavailable = True
                        break
                    self.driver.back()
                    time.sleep(3)
                    self.driver.forward()
                    time.sleep(5)

            if unavailable:
                not_found_data(
                    self.linkedin_url,
                    self.domain,
                    employees_count,
                    self.true_company_title,
                    self.username,
                )
                return "UNAVAILABLE"

            simulate_typing(search_input, key.lower())
            search_input.send_keys(Keys.ENTER)
            time.sleep(5)

            scr = scroll(self.driver, self.wait)
            if scr == "FALSE":
                try:
                    self.driver.find_element(
                        By.XPATH, "//button[contains(.,'Clear all')]"
                    ).click()
                except:
                    self.driver.get(self.driver.current_url.split("?")[0])
                time.sleep(2)
                continue

            finded = self.search_positions(keyword=key, employees_count=employees_count)
            if finded == "FALSE" or finded == "UNAVAILABLE":
                try:
                    self.driver.find_element(
                        By.XPATH, "//button[contains(.,'Clear all')]"
                    ).click()
                except:
                    self.driver.get(self.driver.current_url.split("?")[0])
                time.sleep(2)
            elif not finded:
                try:
                    self.driver.find_element(
                        By.XPATH, "//button[contains(.,'Clear all')]"
                    ).click()
                except:
                    self.driver.get(self.driver.current_url.split("?")[0])
                time.sleep(2)
            else:
                main_finded = True
                if n + 1 != len(self.keyword_data):
                    self.driver.get(self.company_people_url)

        if main_finded == False:
            print("NOT MATCHED!")
            not_found_data(
                self.linkedin_url,
                self.domain,
                employees_count,
                self.true_company_title,
                self.username,
            )

    #
    def add_priority(self, headline):
        if 10 <= self.employee_count < 70:
            for index, posit in enumerate(self.ceo_priority_data['position'].str.lower().str.strip().values):
                if posit in str(headline).lower().strip():
                    selected_row = self.ceo_priority_data.iloc[index]
                    return selected_row['priority']
            return 5000
        if 70 <= self.employee_count <= 400:
            for index, posit in enumerate(self.marketing_priority_data['position'].str.lower().str.strip().values):
                if posit in str(headline).lower().strip():
                    selected_row = self.marketing_priority_data.iloc[index]
                    return selected_row['priority']
            return 5000
        return False

    #
    def start(self):
        remove_old_output(self.output_filename)
        self.driver.get(self.main_url)
        time.sleep(3)
        self.login()
        self.start_empoyee_scan()
        return self.output_filename
        # try:
        #     self.aws_client.upload_output_to_s3(r"./data/output/{}_outdata.csv".format(self.username))
        #     print("output is uploded to aws s3  bucket")
        # except:
        #     print("Faild to upload file s3 bucket ")


# if __name__ == "__main__":
#     config = dotenv_values(".env")
    
#     login_password = {
#         config['USERNAME'] : [config['PASSWORD'], "input/{}_input.csv".format(config['USERNAME'])],
#     }
#     for login, password_file in login_password.items():
#         th1 = threading.Thread(
#             target=LinkedinScraper(login, password_file[0], password_file[1]).start,
#             args=[],
#         )
#         th1.start()
#         th1.join()
#         time.sleep(30)
