from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from .credentials import load_credentials, login
from time import sleep
from datetime import datetime
import os
import sys
from .wait_and_find import *
from random import randint

minRandomJoinLeaveWait = 10
maxRandomJoinLeaveWait = 180

timeOutDelay = 30   # increase if you have a slow internet connection
data = None

maxParticipants = curParticipants = 0
minParticipants = 2

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.notifications": 1 
})

browser = None

def checkAndJoinMeeting():
    global maxParticipants, curParticipants
    joins = wait_and_find_elements_by_xpath(browser, '//button[.="Join"]', 3)
    if len(joins) == 0: # no meeting scheduled
        return
    sleep(randint(minRandomJoinLeaveWait, maxRandomJoinLeaveWait))
    joins[-1].click()   # join the latest meeting scheduled i.e if join buttons for 9 A.M and 10 A.M available, will join 10 A.M
    elem = wait_and_find_element_by_xpath(browser, '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button', timeOutDelay)
    if elem.get_attribute('aria-pressed') == 'true': # turn off camera
        elem.click()
    elem = wait_and_find_element_by_xpath(browser, '//*[@id="preJoinAudioButton"]/div/button', timeOutDelay)
    if elem.get_attribute('aria-pressed') == 'true': # turn off microphone
        elem.click()
    wait_and_find_element_by_xpath(browser, '//button[.="Join now"]', timeOutDelay).click() # join meeting
    print('Joined the meeting at {}'.format(datetime.now()))
    sleep(60*5)
    actions = ActionChains(browser)
    rosterBtn = wait_and_find_element_by_xpath(browser, '//button[@id="roster-button"]', timeOutDelay)
    actions.move_to_element(rosterBtn).click().perform()
    numStr = wait_and_find_elements_by_xpath(browser, '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]')
    if len(numStr) >= 2:
        if numStr[1].text[1:-1] != '':
            maxParticipants = curParticipants = int(numStr[1].text[1:-1])

def checkAndEndOrLeaveOrJoinMeeting():
    global maxParticipants, curParticipants
    hangupBtn = wait_and_find_element_by_xpath(browser, '//button[@id="hangup-button"]', 2)
    if hangupBtn != None: # currently in meeting
        numStr = wait_and_find_elements_by_xpath(browser, '//span[@class="toggle-number"][@ng-if="::ctrl.enableRosterParticipantsLimit"]')
        if len(numStr) >= 2:
            if numStr[1].text[1:-1] != '':
                curParticipants = int(numStr[1].text[1:-1])
            else :
                actions = ActionChains(browser)
                actions.move_to_element(wait_and_find_element_by_xpath(browser, '//button[@id="roster-button"]', timeOutDelay)).click().perform()
        maxParticipants = max(maxParticipants, curParticipants)
        if curParticipants <= minParticipants and curParticipants != 0:   # leaves the meeting automatically for given condition
            sleep(randint(minRandomJoinLeaveWait, maxRandomJoinLeaveWait))
            hangupBtn = wait_and_find_element_by_xpath(browser, '//button[@id="hangup-button"]', 3)
            actions = ActionChains(browser)
            actions.move_to_element(hangupBtn).click().perform()
            print('INFO: Left meeting at {}'.format(datetime.now()))
            browser.get('https://teams.microsoft.com/_#/calendarv2')    # open calendar tab
        else :
            return
    else:  
        maxParticipants = curParticipants = 0
        browser.get('https://teams.microsoft.com/_#/calendarv2')
        checkAndJoinMeeting()

def init(step=0):
    global minParticipants
    browser.get('https://teams.microsoft.com/_#/calendarv2')    # open calendar tab in teams
    sleep(1)
    minParticipants = data.get('minimumParticipants', minParticipants)
    success_step = 0
    # login step
    if step <= 0:
        login(data, check=False, browser=browser)
        success_step = 1
    # calendar access step
    if step <= 1:
        wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay)
        while wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay).get_attribute('name') != "Week": # change calender work-week view to week view
            wait_and_find_element_by_xpath(browser, '//button[@title="Switch your calendar view"]', timeOutDelay).click()
            wait_and_find_element_by_xpath(browser, '//button[@name="Week"]', timeOutDelay).click()
        success_step = 2
    print('INFO: Initialized Succesfully at {}'.format(datetime.now()))
    return success_step

def main():
    global browser, data
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        data = load_credentials(reset=True)    
    else:
        data = load_credentials()
    if data.get("joinMeetingInBackground"):
        opt.add_argument("headless")

    browser = webdriver.Chrome(ChromeDriverManager().install(),options=opt)
 
    step = 0
    while step != 2:
        step = init(step)
    else:
        while True:
            try:
                checkAndEndOrLeaveOrJoinMeeting()
            except:
                print('join meeting failed, trying again')
                browser.get('https://teams.microsoft.com/_#/calendarv2')    # open calendar tab in teams
            else:
                sleep(3)

if __name__ == "__main__":
    main()