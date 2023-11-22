#
from pandas import DataFrame
from time import sleep
#
from email_variations import EmailVariation
from people_to_cheap_helper import (
    csv_to_dict,
    dict_to_list,
    connect_to_sheet,
    send_data_to_sheet,
    people_to_cheap,
    read_from_sheet,
    process_data,
    login_to_gmail,
    add_columns
)
from helper_functions import remove_old_output

#
# https://docs.google.com/spreadsheets/d/1t9ERupBFsBFTATktWj1oruChscGY6xQ67LEaybX2dzI/edit#gid=0
# sudo apt-get install python3-tk python3-dev


#
class PeopleToCheap:
    def __init__(self, login, password, csv_input_filename, json_input_filename, sheet_url, driver):
        self.sheet_url = sheet_url
        self.df = csv_to_dict(csv_input_filename)
        self.mail_variations = EmailVariation(self.df).create_variations()
        self.list_of_mails = dict_to_list(self.mail_variations)
        self.google_acc = connect_to_sheet(json_input_filename)
        self.driver = driver
        self.login = login
        self.password = password
        self.output_filename = "./data/output/{}_outdata_2.csv".format(login)


    def run_script(self):
        remove_old_output(self.output_filename)
        login_to_gmail(self.driver, self.login, self.password)
        self.df = add_columns(self.df)
        for i in range(0, len(self.list_of_mails), 500):
            if i == 0:
                header = True
            else:
                header = True
            send_data_to_sheet(self.google_acc, DataFrame({"email 1": self.list_of_mails[i:i+500], "email 2": self.list_of_mails[i:i+500]}), self.sheet_url)
            sleep(10)
            people_to_cheap(self.driver, self.sheet_url)
            sleep(10)
            df = read_from_sheet(self.google_acc, self.sheet_url)
            self.df = process_data(df, self.mail_variations, self.df, header=header, output=self.output_filename)
        return self.output_filename
        

# #
# if __name__ == "__main__":
#     bot = PeopleToCheap("martin.vardanyan.1996@gmail.com", "SMMNA170696", "./data/output/ruben21294@gmail.com_outdata.csv", "data/input/optify-298517-2cb7358af83f.json", "https://docs.google.com/spreadsheets/d/18Afd_RQTx4MYS_hPpHMwA6aVGtaYneCgZ2yyKjnYA8k/edit#gid=0")
#     bot.run_script()


# https://docs.google.com/spreadsheets/d/1opQeXLblYKl9EhqjNVQN44uIjg2-qKbY-4zYUK2UyIU/edit#gid=921194321