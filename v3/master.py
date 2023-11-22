#
from dotenv import dotenv_values
import undetected_chromedriver as uc


#
from LinkedIn_people_finder import LinkedinScraper
from LinkedIn_people_finder_part2 import LinkedinScraperPart2
from people_to_cheap import PeopleToCheap


#
class MasterBot:
    #
    def __init__(
            self,
            linkedin_username,
            linkedin_password,
            gmail_username,
            gmail_password,
            sheet_url,
            json_file
            ):
        self.linkedin_username = linkedin_username
        self.linkedin_password = linkedin_password
        self.gmail_username = gmail_username
        self.gmail_password = gmail_password
        self.chrome_options = uc.ChromeOptions()
        self.chrome_options.add_argument("--start-maximized")
        self.driver = uc.Chrome(
            driver_executable_path="./driver/chromedriver", options=self.chrome_options
        )
        self.sheet_url = sheet_url
        self.json_file = json_file
        self.input_filename = "./data/input/{}_input.csv".format(self.linkedin_username)

    #
    def step_1(self):
        step1 = LinkedinScraper(
            self.linkedin_username,
            self.linkedin_password,
            self.input_filename,
            self.driver
            )
        output_filename = step1.start()
        return output_filename

    #
    def step_2(self, input_filename):
        step2 = PeopleToCheap(
            self.gmail_username,
            self.gmail_password,
            input_filename,
            self.json_file,
            self.sheet_url,
            self.driver
        )
        output_filename = step2.run_script()
        return output_filename

    #
    def step_3(self, input_filename):
        step3 = LinkedinScraperPart2(
            self.linkedin_username,
            self.linkedin_password,
            input_filename,
            self.input_filename,
            self.driver
            )
        output_file_name = step3.start()
        return output_file_name

    #
    def check_favorite(self, file_name):
        LinkedinScraperPart2.check_output(file_name)

    #
    def run_script(self):
        step2_input = self.step_1()
        step3_input = self.step_2(step2_input)
        output_name = self.step_3(step3_input)
        self.check_favorite(output_name)


#
if __name__ == "__main__":
    config = dotenv_values(".env")
    linkedin_username = config['LINKEDIN_USERNAME']
    linkedin_password = config['LINKEDIN_PASSWORD']
    gmail_username = config['GMAIL_USERNAME']
    gmail_password = config['GMAIL_PASSWORD']
    json_file = "data/input/optify-298517-2cb7358af83f.json"
    sheet_url = "https://docs.google.com/spreadsheets/d/18Afd_RQTx4MYS_hPpHMwA6aVGtaYneCgZ2yyKjnYA8k/edit#gid=0"
    master_bot = MasterBot(
        linkedin_username,
        linkedin_password,
        gmail_username,
        gmail_password,
        sheet_url,
        json_file
        )
    master_bot.run_script()
