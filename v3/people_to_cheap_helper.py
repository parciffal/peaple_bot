import gspread
import pyautogui
import pandas as pd
from time import sleep
from random import randint
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


#
def connect_to_sheet(input_json):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        input_json, scopes
    )
    acc = gspread.authorize(credentials)
    return acc

#
def send_data_to_sheet(acc, data, sheet_url):
    sheet = acc.open_by_url(sheet_url).sheet1
    sheet.clear()
    set_with_dataframe(sheet, data)
    return True


#
def find_position(email, dct):
    for key in dct:
        if email in dct[key]:
            return key, dct[key].index(email)
    return False, False


#
def add_columns(df):
    df['Favorite'] = ["" for _ in range(len(df))]
    for i in range(1, 9):
        column_name = f'Variant {i}'
        df[column_name] = ["" for _ in range(len(df))]
    return df

#
def favorite(df):
    # Not favorite if priority == min_value
    min_priority = df.groupby("original domain")['priority'].transform('min')
    df["Favorite"] = ["Favorite" if priority == min_val and min_val < 5000 else "Not Favorite" for priority, min_val in zip(df["priority"], min_priority)]
    return df

#
def post_data(df, header, output):
    df = favorite(df)
    df.to_csv(output, index=False, header=header, encoding="utf-8")
   

#
def process_data(df, mail_variations, finish_df, header, output):
    print("LEN OF DF", len(df.index))
    for _, row in df.iterrows():
        if row['result'] == "FALSE":
            pos, _ = find_position(row['email 1'], mail_variations)
            if type(pos) is bool:
                continue
            else:   
                if finish_df.loc[pos, f"Variant 1"]:
                    if finish_df.loc[pos, f"Variant 2"]:
                        if finish_df.loc[pos, f"Variant 3"]:
                            if finish_df.loc[pos, f"Variant 4"]:
                                if finish_df.loc[pos, f"Variant 5"]:
                                    if finish_df.loc[pos, f"Variant 6"]:
                                        if finish_df.loc[pos, f"Variant 7"]:
                                            if finish_df.loc[pos, f"Variant 8"]:
                                                continue
                                            else:
                                                finish_df.at[pos, f"Variant 8"] = row['email 1']
                                        else:
                                            finish_df.at[pos, f"Variant 7"] = row['email 1']
                                    else:
                                        finish_df.at[pos, f"Variant 6"] = row['email 1']
                                else:
                                    finish_df.at[pos, f"Variant 5"] = row['email 1']
                            else:
                                finish_df.at[pos, f"Variant 4"] = row['email 1']
                        else:
                            finish_df.at[pos, f"Variant 3"] = row['email 1']
                    else:
                        finish_df.at[pos, f"Variant 2"] = row['email 1']    
                else:
                    finish_df.at[pos, f"Variant 1"] = row['email 1']
                post_data(finish_df, header=header, output=output)
        else:
            continue
    return finish_df


#
def read_from_sheet(acc, sheet_url):
    sheet = acc.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    df = pd.DataFrame.from_dict(data)
    return df


#
def login_to_gmail(driver, login, password):
    driver.get("https://mail.google.com/")
    input_login = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
    input_login.send_keys(login)
    _next = driver.find_element(
        By.XPATH, '//*[@id="identifierNext"]/div/button/span'
    )
    _next.click()
    sleep(15)
    input_password = driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
    )
    input_password.send_keys(password)
    _next = driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span')
    _next.click()
    sleep(30)


#
def people_to_cheap(driver, sheet_url):
    driver.get(sheet_url)
    sleep(5)
    for i in range(2):
        pyautogui.hotkey("ctrl", "left")
        sleep(randint(1,2))
    pyautogui.hotkey("ctrl", "up")
    sleep(randint(1,2))
    pyautogui.hotkey("ctrl", "space")
    sleep(randint(1,2))
    pyautogui.hotkey("alt", "i")
    sleep(randint(1,2))
    pyautogui.press("a")
    sleep(randint(1,2))
    pyautogui.press("e")
    # WAIT FOR CHECKING
    sleep(10)
    pyautogui.press("right")
    sleep(randint(1,2))
    pyautogui.press("right")
    sleep(randint(1,2))
    pyautogui.write('result', interval=0.25)
    sleep(randint(1,2))
    pyautogui.press('down')
    sleep(randint(1,2))
    pyautogui.write("=a2=b2")
    sleep(randint(1,2))
    pyautogui.press("enter")
    sleep(randint(1,2))
    pyautogui.press("up")
    sleep(randint(1,2))
    pyautogui.hotkey("ctrl", "c")
    sleep(randint(1,2))
    pyautogui.hotkey("ctrl", "shift", "down")
    sleep(randint(1,2))
    pyautogui.hotkey("ctrl", "v")
    sleep(randint(1,2))
    #pyautogui.hotkey("ctrl","down")
    #sleep(randint(1,2))
    #pyautogui.press('left')
    #sleep(randint(1,2))
    #pyautogui.hotkey('ctrl', "up")
    #sleep(randint(1,2))
    #pyautogui.press("down")
    #sleep(randint(1,2))
    #pyautogui.press("right")
    #sleep(randint(1,2))
    #pyautogui.hotkey('ctrl', "shift", 'down')
    #sleep(randint(1,2))
    #pyautogui.press('backspace')
    #sleep(randint(1,2))
    #for i in range(3):
    #    pyautogui.hotkey('ctrl', "up")
    #    sleep(randint(1,2))


#
def init_selenium():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    driver = uc.Chrome(
            driver_executable_path="./driver/chromedriver", options=chrome_options
        )
    return driver

#
def csv_to_dict(file):
    in_data = pd.read_csv(file)
    return in_data


#
def dict_to_list(dct):
    res = []
    for key in dct:
        res.extend(dct[key])
    return res


#
def create_posistion_csv(input_file):
    df = pd.read_csv(input_file)
    positions = df['position_1'].dropna()
    final_positions = []
    for pos in positions:
        comma_split = pos.split(",")
        for com_spl in comma_split:
            _positions = com_spl.split("=")
            for one_pos in _positions:
                if one_pos.strip() not in final_positions:
                    final_positions.append(one_pos.strip())

    pd.DataFrame({"position":final_positions, "priority": [i+1 for i in range(len(final_positions))]}).to_csv("position_priority.csv", index=False)
    return True

# create_posistion_csv("data/input_2.csv")