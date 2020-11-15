from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ExpConditions
from selenium.webdriver.common.by import By
from time import sleep
import re

# initialize web_driver object in a variable
# initialize web_driver object in a variable
profile = webdriver.FirefoxProfile("C:/Users/shameem/AppData/Roaming\Mozilla/Firefox/Profiles/automate")
web_browser = webdriver.Firefox(firefox_profile=profile)

XPTH_CUSTOMER_ASSESTS_AND_ENTITLEMENTS = "//div[@role='presentation']//ul[@aria-label='Case Form']//li[@data-id='tablist-CustomerInformation_16']"
ID_NOTES_HISTORY_TEXT_AREA = "txtNotesHistory"
XPATH_NOTES_HISTORY_IFRAME = "//div[@data-id='WebResource_NotesHistory-webResourceLabelControlWrapper']//iframe[@id]"
XPATH_NOTES_AND_INFORMATION = "//div[@role='presentation']//ul[@aria-label='Case Form']//li[@data-id='tablist-NotesAndInformation']"
XPATH_CASE_CLICK = "//div[@title][@role='gridcell' and @data-id='cell-{}-2']//a[@title]"
ID_PROGRESS_INDICATOR = "progressIndicatorContainer"

LOGIN_FORM = "loginfmt"
BASE_URL = "https://hpcdax.crm.dynamics.com/main.aspx?appid=c4ac64fc-8e58-e911-a83c-000d3a3b7d47&pagetype=entitylist&etn=queueitem"
# BASE_URL = "https://hpcdax.crm.dynamics.com/"
USERNAME_ID = "username"
USER_PASSWORD_ID = "password"
user_email = "naym@hp.com"
user_password = "Ayaan@0606"
SUBMIT_CHECK_BOX = "//input[@type='submit']"
DONT_SHOW_AGAIN = "DontShowAgain"
XPATH_SWITCH_TO_ANOTHER_APP = "//a[@title='Switch to another app']"
XPATH_HPI_SERVICES = "//span[text() = 'HPI Services']"

XPATH_QUEUE_IMAGE_CLICK = "//img[@title='Queues']"
XPATH_SEARCH_QUEUE = "//input[starts-with(@id,'undefined_')]"
QUEUE_NAME = "<SPY_ES DOA>"
XPATH_DATA_ROW_COUNT = "//div[@data-row-count]"
ATTRIBUTE_DATA_ROW_COUNT = "data-row-count"

refresh_times = 2
refresh_times_while = 1
# sleep constants
VERY_SHORT_WAIT = 1
SHORT_WAIT = 2
LONG_WAIT = 5
VERY_LONG_WAIT = 10
LONGEST_WAIT = 15
# wait_constants
WAIT_ONE_MINUTE = 60
WAIT_TWO_MINUTES = 120
WAIT_FIVE_MINUTES = 300
WAIT_TEN_MINUTES = 3000
invisibility_condition = WebDriverWait(web_browser, 120).until(
    ExpConditions.invisibility_of_element_located(
        (By.ID, ID_PROGRESS_INDICATOR)))
WebDriverWait(web_browser, 120).until(
    ExpConditions.visibility_of_all_elements_located((By.XPATH, XPATH_DATA_ROW_COUNT)))

queues_click = WebDriverWait(web_browser, 120).until(
    ExpConditions.element_to_be_clickable((By.XPATH, XPATH_QUEUE_IMAGE_CLICK)))
queues_click.click()
condition = ExpConditions.visibility_of_element_located((By.XPATH,
                                                         XPATH_SEARCH_QUEUE))
search_option = WebDriverWait(web_browser, 120).until(condition)
search_option.click()
search_option.clear()
search_option.send_keys(QUEUE_NAME)
search_option.send_keys(Keys.DOWN, Keys.ENTER)
sleep(300)

rows = web_browser.find_element_by_xpath(XPATH_DATA_ROW_COUNT).get_attribute(ATTRIBUTE_DATA_ROW_COUNT)
# main for loop to open the case for loop
for row in range(int(rows)):
    # check for the title of the case it to wait a maximum of 2 minutes\
    invisibility_condition = WebDriverWait(web_browser, 120).until(
        ExpConditions.invisibility_of_element_located(
            (By.ID, ID_PROGRESS_INDICATOR)))

    # Progress Indicator
    if invisibility_condition:
        WebDriverWait(web_browser, 120).until(
            ExpConditions.element_to_be_clickable((By.XPATH, XPATH_CASE_CLICK.format(row))))
        # click on the title to open the case page

        web_browser.find_element_by_xpath(XPATH_CASE_CLICK.format(row)).click()
        case_id = web_browser.find_element_by_xpath(XPATH_CASE_CLICK.format(row)).text
        print(case_id)

    # wait for the element to be click able
    WebDriverWait(web_browser, 120).until(
        ExpConditions.visibility_of_all_elements_located((By.XPATH, XPATH_NOTES_AND_INFORMATION)))
    web_browser.find_element_by_xpath(XPATH_NOTES_AND_INFORMATION).click()

    try:
        WebDriverWait(web_browser, 120).until(
            ExpConditions.visibility_of_element_located((By.XPATH, XPATH_NOTES_HISTORY_IFRAME)))
        notes_history_frame = web_browser.find_element_by_xpath(XPATH_NOTES_HISTORY_IFRAME)
        web_browser.switch_to.frame(notes_history_frame)

        WebDriverWait(web_browser, 120).until(
            ExpConditions.element_to_be_clickable((By.ID, ID_NOTES_HISTORY_TEXT_AREA)))
        notes_by_agent = web_browser.find_element(By.ID, ID_NOTES_HISTORY_TEXT_AREA).text

        remove_every_special_character_pattern = re.compile('[\W\d\s_]+')
        cleaned_text = remove_every_special_character_pattern.sub(' ', notes_by_agent)

        check_string_pattern = re.compile(r'''(((claim)+\s(type)+)+\s # claim followed by space followed by type then space case incensitive

                                                  ((replacement)+|(credit)+)+\s # replacement or credit followed by one or more space

                                                  (from)+\s # from one or more times followed by space

                                                  ((reseller)+|(distributor)+)+)+ # reseller or distributor one or more time ''',
                                          re.IGNORECASE | re.VERBOSE)
        print("just before if")
        if check_string_pattern.search(cleaned_text):
            print("Success")
            web_browser.switch_to.default_content()
            web_browser.find_element_by_xpath(XPTH_CUSTOMER_ASSESTS_AND_ENTITLEMENTS)
            web_browser.back()
        else:
            print("fail")
            web_browser.switch_to.default_content()
            WebDriverWait(web_browser, 120).until(
                ExpConditions.visibility_of_all_elements_located(
                    (By.XPATH, XPTH_CUSTOMER_ASSESTS_AND_ENTITLEMENTS)))
            web_browser.find_element_by_xpath(XPTH_CUSTOMER_ASSESTS_AND_ENTITLEMENTS).click()
            web_browser.back()
        print("Outside of else")

        # print(str(row) + ") Case number... " + str(row) + "\n" + notes_by_agent)
        print("\n")

        # 12 | selectFrame | relative=parent


    # web_browser.switch_to.default_content()
    # web_browser.back()
    except TimeoutException:
        print("An timeout exception occurred")

title = web_browser.find_element_by_tag_name("title").text