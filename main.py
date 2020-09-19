import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import Select

from utils import *
from constants import *

# config options for selenium driver. These include:
# a fake user agent
# prevent chrome detection that we are using Selenium
# prevent remember login info modal form popup
options = Options()
ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument('user-agent={userAgent}')
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
prefs = {"credentials_enable_service", False}
prefs = {"profile.password_manager_enabled" : False}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options, executable_path='D:\ChromDriver\chromedriver.exe')
url = driver.command_executor._url
print(url)
session_id = driver.session_id
print(session_id)

class WebTable:
    def __init__(self, webtable_path):
       self.path = webtable_path

    def get_row_count(self):
        return len(driver.find_elements_by_xpath(self.path + "/tbody/tr"))

    def get_column_count(self):
        return len(driver.find_elements_by_xpath(self.path + '/tbody/tr[1]/td'))

    def get_table_size(self):
        return {"rows": self.get_row_count(),
                "columns": self.get_column_count()}

    def row_data(self, row_number):
        row = driver.find_elements_by_xpath(self.path + "/tbody/tr["+str(row_number)+"]/td")
        rData = []
        for webElement in row :
            rData.append(webElement.text)
        return rData

    def column_data(self, column_number):
        col = driver.find_elements_by_xpath(self.path + "/tbody/tr/td["+str(column_number)+"]")
        rData = []
        for webElement in col :
            rData.append(webElement.text)
        return rData

    def get_all_data(self):
        # get number of rows
        noOfRows = self.get_row_count()
        # get number of columns
        noOfColumns = self.get_column_count()
        allData = []
        # iterate over the rows, to ignore the headers we have started the i with '1'
        for i in range(1, noOfRows+1):
            # reset the row data every time
            ro = []
            # iterate over columns
            for j in range(1, noOfColumns+1) :
                # get text from the i th row and j th column
                # sometime the row is empty, we just append an empty string
                try:
                    ro.append(driver.find_element_by_xpath(self.path + "/tbody/tr["+str(i)+"]/td["+str(j)+"]").text)
                except:
                    ro.append('')
            # add the row data to allData of the self.table
            allData.append(ro)

        return allData

    def click_on_view_detail(self, row_number):
        view_detail_column_number = 8
        current_cell = driver.find_element_by_xpath(self.path + "/tbody/tr["+str(row_number)+"]/td["+str(view_detail_column_number)+"]")
        link_to_click = current_cell.find_element_by_tag_name("a")
        link_to_click.click()
        time.sleep(10)

    def click_on_row(self, row_number):
        row = driver.find_element_by_xpath(self.path + "/tbody/tr["+str(row_number)+"]/td[1]")
        row.click()
        time.sleep(3)

    def presence_of_data(self, data):
        # verify the data by getting the size of the element matches based on the text/data passed
        dataSize = len(driver.find_elements_by_xpath(self.path + "/tbody/td[normalize-space(text())='"+data+"']"))
        presence = False
        if(dataSize > 0):
            presence = true
        return presence

    def get_cell_data(self, row_number, column_number):
        if (row_number == 0):
            raise Exception("Row number starts from 1")

        cellData = driver.find_element_by_xpath(self.path + "/tbody/tr["+str(row_number)+"]/td["+str(column_number)+"]").text
        return cellData

def login():
    # Sleep
    time.sleep(5)
    # select country
    country_select = Select(driver.find_element_by_xpath('//*[@id="country-select"]'))
    country_select.select_by_value('US')
    # Hit submit
    submit_btn = driver.find_element_by_xpath('//*[@id="submit-button"]')
    submit_btn.submit()
    time.sleep(3)
    # Enter login info
    driver.find_element_by_xpath('//*[@id="loginForm-email-input"]').send_keys('arne9131@gmail.com')
    driver.find_element_by_xpath('//*[@id="loginForm-password-input"]').send_keys('@esx5099')
    driver.find_element_by_xpath('//*[@id="loginForm-submit-button"]').submit()
    time.sleep(5)

def main():
    # first log in
    login()
    # Click on patient dashboard
    driver.find_element_by_xpath('//*[@id="main-header-dashboard-icon"]').click()
    time.sleep(3)
    # Get all the patients info
    try:
        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="app-content"]/div[1]/div/div[2]/div[1]/div/div[1]/table')))
        if (table):
            patients_table = WebTable('//*[@id="app-content"]/div[1]/div/div[2]/div[1]/div/div[1]/table')
            print(patients_table.get_table_size())
            print(patients_table.get_all_data())

            num_of_rows = patients_table.get_row_count()
            for row_num in range(1, num_of_rows + 1):
                patients_table.click_on_row(row_num)
                # Click on glucose report btn
                driver.find_element_by_xpath('//*[@id="pastGlucoseCard-report-button"]').click()
                time.sleep(5)
                # Click on monthly summary menu
                driver.find_element_by_xpath('//*[@id="20-select-report-button-container"]').click()
                time.sleep(3)
                open_new_window_for_svg_crawling()
                time.sleep(3)
                crawl_svg_calendar()
                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
                driver.execute_script("window.history.go(-1)")
                time.sleep(2)
    except:
        return

def open_new_window_for_svg_crawling():
    driver.switch_to.default_content()
    all_frames = driver.find_elements_by_xpath("//iframe[@title='reportFrame']")
    print('count', len(all_frames))
    monthly_frame = all_frames[6]
    src = monthly_frame.get_attribute("src")
    print('src', src)
    #url = urljoin(base_url, src)
    driver.get(src)
    #driver.switch_to.frame(monthly_frame)

    time.sleep(3)
    date_shown = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.ID, 'dateTag'))).text
    print('date', date_shown)

    all_texts = driver.find_elements_by_xpath('//*[@id="monthlySummaryChartArea"]/*[name()="svg"]/*[name()="text"]')
    for i in range(len(all_texts)):
        print(i, all_texts[i].text)

def crawl_svg_calendar():
    all_texts = driver.find_elements_by_xpath('//*[@id="monthlySummaryChartArea"]/*[name()="svg"]/*[name()="text"]')
    for i in range(len(all_texts)):
        print(i, all_texts[i].text)

    date_shown = driver.find_elements_by_id('dateTag')
    try:
        date_obj = convert_to_datetime_obj(DATE_TO_CRAWL)
        month_year = date_obj.strftime('%B %Y')
        day = date_obj.strftime('%d')
        if (day[0] == '0'):
            day = day[1]

        # find index of the month that matches with date
        date_shown = [item.text for item in date_shown]
        index = date_shown.index(month_year)

        cntr = 0
        all_texts = [item.text for item in all_texts]
        while (all_texts[cntr + 1] != 'Monday') and (index > 0):
            cntr += 1

        # jump over all the days
        cntr = cntr + 8

        # Now we are in the correct month
        done = False
        idx = 0
        while not done:
            idx = all_texts.index(day, cntr)
            if (all_texts[idx+1] != 'mg/dL'):
                print('Level', all_texts[idx+1])
                print('value', all_texts[idx+2])
                print('freq', all_texts[idx+4])
                done = True
            else:
                cntr = idx
    except:
        return ''

if __name__ == '__main__':
    driver.get('https://www.libreview.com')
    #driver = webdriver.Remote(command_executor='http://127.0.0.1:53685',desired_capabilities={})
    #driver.close()   # this prevents the dummy browser
    #driver.session_id = '33ce67b414639d5c60ae506bd67fa314'
    main()