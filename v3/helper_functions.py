#
import os
import re
import string
import time
import random
import pandas as pd
import numpy as np

#
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


#
def check_word(text):
    bla = {
        "À": "a",
        "Á": "a",
        "Â": "a",
        "Ã": "a",
        "Ä": "a",
        "Å": "a",
        "Æ": "a",
        "à": "a",
        "á": "a",
        "â": "a",
        "ã": "a",
        "ä": "a",
        "å": "a",
        "æ": "a",
        "Ā": "a",
        "ā": "a",
        "Ă": "a",
        "ă": "a",
        "Ą": "a",
        "ą": "a",
        "Ç": "c",
        "ç": "c",
        "Ć": "c",
        "ć": "c",
        "Ĉ": "c",
        "ĉ": "c",
        "Ċ": "c",
        "ċ": "c",
        "Č": "c",
        "č": "c",
        "Ď": "d",
        "ď": "d",
        "Đ": "d",
        "đ": "d",
        "È": "e",
        "É": "e",
        "Ê": "e",
        "Ë": "e",
        "è": "e",
        "é": "e",
        "ê": "e",
        "ë": "e",
        "ð": "e",
        "Ē": "e",
        "ē": "e",
        "Ĕ": "e",
        "ĕ": "e",
        "Ė": "e",
        "ė": "e",
        "Ę": "e",
        "ę": "e",
        "Ě": "e",
        "ě": "e",
        "Ĝ": "g",
        "ĝ": "g",
        "Ğ": "g",
        "ğ": "g",
        "Ġ": "g",
        "ġ": "g",
        "Ģ": "g",
        "ģ": "g",
        "Ĥ": "h",
        "ĥ": "h",
        "Ħ": "h",
        "ħ": "h",
        "Ì": "i",
        "Í": "i",
        "Î": "i",
        "Ï": "i",
        "ì": "i",
        "í": "i",
        "î": "i",
        "ï": "i",
        "Ĩ": "i",
        "ĩ": "i",
        "Ī": "i",
        "ī": "i",
        "Ĭ": "i",
        "ĭ": "i",
        "Į": "i",
        "į": "i",
        "İ": "i",
        "ı": "i",
        "Ĳ": "i",
        "ĳ": "i",
        "Ĵ": "j",
        "ĵ": "j",
        "Ķ": "k",
        "ķ": "k",
        "ĸ": "k",
        "Ĺ": "l",
        "ĺ": "l",
        "Ļ": "l",
        "ļ": "l",
        "Ľ": "l",
        "ľ": "l",
        "Ŀ": "l",
        "ŀ": "l",
        "Ł": "l",
        "ł": "l",
        "Ñ": "n",
        "ñ": "n",
        "Ń": "n",
        "ń": "n",
        "Ņ": "n",
        "ņ": "n",
        "Ň": "n",
        "ň": "n",
        "ŉ": "n",
        "Ŋ": "n",
        "ŋ": "n",
        "Ò": "o",
        "Ó": "o",
        "Ô": "o",
        "Õ": "o",
        "Ö": "o",
        "Ø": "o",
        "ò": "o",
        "ó": "o",
        "ô": "o",
        "õ": "o",
        "ö": "o",
        "ø": "o",
        "Ō": "o",
        "ō": "o",
        "Ŏ": "o",
        "ŏ": "o",
        "Ő": "o",
        "ő": "o",
        "Œ": "o",
        "œ": "o",
        "Þ": "p",
        "þ": "p",
        "Ŕ": "r",
        "ŕ": "r",
        "Ŗ": "r",
        "ŗ": "r",
        "Ř": "r",
        "ř": "r",
        "ß": "s",
        "Ś": "s",
        "ś": "s",
        "Ŝ": "s",
        "ŝ": "s",
        "Ş": "s",
        "ş": "s",
        "Š": "s",
        "š": "s",
        "ſ": "s",
        "Ţ": "t",
        "ţ": "t",
        "Ť": "t",
        "ť": "t",
        "Ŧ": "t",
        "ŧ": "t",
        "Ù": "u",
        "Ú": "u",
        "Û": "u",
        "Ü": "u",
        "ù": "u",
        "ú": "u",
        "û": "u",
        "ü": "u",
        "Ũ": "u",
        "ũ": "u",
        "Ū": "u",
        "ū": "u",
        "Ŭ": "u",
        "ŭ": "u",
        "Ů": "u",
        "ů": "u",
        "Ű": "u",
        "ű": "u",
        "Ų": "u",
        "ų": "u",
        "Ŵ": "w",
        "ŵ": "w",
        "Ý": "y",
        "ý": "y",
        "ÿ": "y",
        "Ŷ": "y",
        "ŷ": "y",
        "Ÿ": "y",
        "Ź": "z",
        "ź": "z",
        "Ż": "z",
        "ż": "z",
        "Ž": "z",
        "ž": "z",
    }
    for key, value in bla.items():
        if key in text:
            text = text.replace(key, value)
    return text[0].upper() + text[1:]


#
def remove_punctuation(text):
    cleaned_text = "".join(c for c in text if c not in string.punctuation)
    return cleaned_text


#
def remove_text_in_parentheses(text):
    cleaned_text = ""
    inside_parentheses = False

    for c in text:
        if c == "(":
            inside_parentheses = True
        elif c == ")":
            inside_parentheses = False
            continue

        if not inside_parentheses:
            cleaned_text += c

    return cleaned_text


#
def remove_emojis(text):
    emoji_pattern = re.compile(
        pattern="["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "]+",
        flags=re.UNICODE,
    )
    cleaned_text = emoji_pattern.sub(r"", text)
    return cleaned_text


#
def process_string(text):
    text_without_parentheses = remove_text_in_parentheses(text)
    text_without_emojis = remove_emojis(text_without_parentheses)
    cleaned_text = remove_punctuation(text_without_emojis)
    return cleaned_text


#
def csv_to_dict(file):
    print(file)
    in_data = pd.read_csv(file)
    return in_data


#     
def simulate_typing(element, text):
    for i in text:
        time.sleep(random.uniform(0, 0.5))
        element.send_keys(i)


#
def scroll_to_bottom(driver):
    old_position = 0
    new_position = None

    while new_position != old_position:
        old_position = driver.execute_script(
            (
                "return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"
            )
        )
        time.sleep(1)
        driver.execute_script(
            (
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"
            )
        )
        new_position = driver.execute_script(
            (
                "return (window.pageYOffset !== undefined) ?"
                " window.pageYOffset : (document.documentElement ||"
                " document.body.parentNode || document.body);"
            )
        )


#
def check_company_size(employee_count):
    if employee_count > 200:
        return True
    else:
        return False

#
def check_unavailable(driver):
    if "unavailable" in driver.current_url:
        return True
    return False

#
def artdeco_card__with_hover(driver, wait, employee_count, unavailable):
    y = 0
    link_positions = []
    while True:
        if y == 2:
            unavailable = True
            break
        try:
            link_positions = wait.until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "artdeco-card--with-hover")
                )
            )
            break
        except TimeoutException:
            y += 1
            print("TIMEOUT EXCEPTION")
            if check_unavailable(driver):
                unavailable = True
                break
            driver.back()
            time.sleep(3)
            driver.forward()
            time.sleep(5)
            scroll(driver, employee_count)
            continue
    return link_positions, unavailable


#
def not_found_data(linkedin_url, domain, employees_count, true_company_title, username):
    out_data = {
        "original domain": domain,
        "linkedinUrl": "Not found",
        "fullName": "Not Found",
        "name": "Not Found",
        "surname": "Not Found",
        "url": linkedin_url,
        "good": "Not Found",
        "position": "Not Found",
        "keyword": "Not Found",
        "employee count": employees_count,
        "company name": true_company_title,
        "country": "Not Found",
        "email": "Not Found",
        "priority": 5000,
        "favorite": "Not favorite",
        "fake": "Not Found",
        "domain": "",
        "variant 1": "",
        "variant 2": "",
        "variant 3": "",
        "variant 4": "",
        "variant 5": "",
        "variant 6": "",
        "variant 7": ""
    }
    dict_to_csv(out_data, username, "1")


#   
def get_employee_count(driver, wait):
    n = 0
    while True:
        if n == 2:
            return False
        try:
            el = wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "text-heading-xlarge")
                )
            )
            employee_count = int(el.text.split()[0])
            return employee_count
        except:
            print("TIMEOUT EXCEPTION")
            if check_unavailable(driver):
                return False
            driver.back()
            time.sleep(3)
            driver.forward()
            time.sleep(5)
        n += 1


#
def scroll(driver, wait):
    driver.execute_script("document.body.style.zoom='60%'")
    employee_count = get_employee_count(driver, wait)
    time.sleep(2)
    if employee_count:
        for i in range(int(employee_count / 10)):
            driver.execute_script("window.scrollBy(0, -200);")
            scroll_to_bottom(driver)
            time.sleep(random.uniform(1, 2))
        time.sleep(2)
    else:
        return "False"
    

#
def dict_to_csv(dict, username, number):
    df = pd.DataFrame([dict])
    if not os.path.isfile(r"./data/output/{}_outdata_{}.csv".format(username, number)):
        df.to_csv(r"./data/output/{}_outdata_{}.csv".format(username, number), index=False, header=True, encoding="utf-8")
    else:
        df.to_csv(
            r"./data/output/{}_outdata_{}.csv".format(username, number),
            index=False,
            mode="a",
            header=False,
            encoding="utf-8"
        )

#
def remove_old_output(filename):
    try:
        os.remove(filename)
    except:
        pass

#
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

#
def drop_empty_rows(df, column):
    df[column].replace('', np.nan, inplace=True)
    df.dropna(subset=[column], inplace=True)
    return df

#
def final_part(driver, wait, pattern, username, init_data):
    df = pd.read_csv(r"./data/output/{}_outdata.csv".format(username))
    for index, row in df.iterrows():
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
                try:
                    df.at[index, "linkedinUrl"] = original_linkedin_url
                except:
                    df.at[index, "linkedinUrl"] = "Not found"
                df.at[index, "domain"] = link.split("/")[0]
                df.to_csv(r"data/output/{}_outdata.csv".format(username), index=False, encoding="utf-8")
            else:
                continue
        else:
            filtered_df = init_data[init_data['company'] == row['linkedinUrl']]
            try:
                original_linkedin_url = filtered_df['linkedinUrl'].tolist()[0]
            except:
                original_linkedin_url = "Not found"
    df.drop_duplicates()
    df = drop_empty_rows(df, "domain")
    df.to_csv(r"data/output/{}_outdata.csv".format(username), index=False, encoding="utf-8")
    return True
