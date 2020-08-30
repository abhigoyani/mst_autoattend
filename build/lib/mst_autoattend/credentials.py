import pathlib
import json
from wait_and_find import *
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

timeOutDelay = 30   # increase if you have a slow internet connection

CREDENTIALS_FILE_PATH = pathlib.Path.home() / '.msteams_class_attender'

def login(data, check=False, browser=None):
    if check:
        opt = Options()
        # opt.add_argument("headless")
        browser = webdriver.Chrome(ChromeDriverManager().install(),options=opt)
        browser.get('https://teams.microsoft.com/_#/calendarv2')
    wait_and_find_ele_by_id(browser, 'i0116', timeOutDelay).send_keys(data['username'])      # enter username
    wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click next
    wait_and_find_ele_by_id(browser, 'aadTile', timeOutDelay).click()                        # choose organization account
    wait_and_find_ele_by_id(browser, 'i0118', timeOutDelay).send_keys(data['password'])      # enter password
    wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click next
    pass_error = wait_and_find_ele_by_id(browser, 'passwordError', timeOutDelay)
    if pass_error is not None:
        raise Exception(pass_error.get_attribute("innerHTML"))
    if not check:
        wait_and_find_ele_by_id(browser, 'idSIButton9', timeOutDelay).click()                    # click yes to stay signed in
    else:
        browser.quit()

def load_credentials(reset=False):
    modified = False
    data = {}
    if not reset:
        try:
            with open(CREDENTIALS_FILE_PATH) as f:
                data = json.load(f)
            print("DEBUG: Saved credentials loaded!")
            if data.get("username") is None:
                data['username'] = input("Please enter your MS Teams username: ")
                modified = True
            if data.get("password") is None:
                data["password"] = input("Please enter your MS Teams password: ")
                modified = True
        except (FileNotFoundError, json.JSONDecodeError):
            print("DEBUG: Failed to load from credentials file!")
            reset = True
    if (reset):
        login_success = False
        while not login_success:
            data['username'] = input("Please enter your MS Teams username: ")
            data["password"] = input("Please enter your MS Teams password: ")
            try:
                print("INFO: Verifying username and password, please wait for a few minutes...")
                login(data, True)
                login_success = True
                print("INFO: Authentication Success!")
            except:
                print("ERROR: Authentication Failed!")
                continue
            data["minimumParticipants"] = input("Please enter minimum participants to exit the meeting: ")
            response = input("Do you want to interact in the meeting while it is going on? (y/n): ")
            while response.lower() not in ["y", "n"]:
                print("ERROR: Please enter y or n!")
                response = input("Do you want to interact in the meeting while it is going on? (y/n): ")
            if response.lower() == "y":
                data["joinMeetingInBackground"] = False
            else:
                data["joinMeetingInBackground"] = True
        modified = True

    if modified:
        with open(CREDENTIALS_FILE_PATH, "x") as f:
            json.dump(data, f)
        print("DEBUG: Credentials saved to " + str(CREDENTIALS_FILE_PATH))
    return data
