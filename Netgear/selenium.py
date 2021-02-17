"""
This script is automating the Netgear AP series WAC5xx web ui through selenium and automatically setting  channel to 36

Date- 16- feb - 2021
-Nikita Yadav 
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
def main():
    browser = webdriver.Chrome('C:\Program Files\Google\Chrome\Application\chromedriver')
    browser.get('https://192.168.200.194')

    error = browser.find_element_by_id('details-button')
    error.click()
    proceed = browser.find_element_by_id('proceed-link')
    proceed.click()
    time.sleep(5)

    try:
        username = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "userName")))
        username.send_keys('admin')
        paswd = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "userPwd")))
        paswd.send_keys('Netgear@123')
        login = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "enter")))
        login.click()
        time.sleep(10)
        management = WebDriverWait(browser, 40).until(EC.presence_of_element_located((By.LINK_TEXT, "Management")))
        management.click()
        time.sleep(30)
        wireless = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="demo3"]/li/a[3]')))
        wireless.click()
        time.sleep(2)
        basic = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="SubMenu3"]/li[1]/a')))
        basic.click()
        time.sleep(10)
        wireless_settings = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/section/div/div/div/div/div/ul/li[2]/a')))
        wireless_settings.click()
        time.sleep(10)
        channel = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="channelWlan1"]')))
        channel.click()
        time.sleep(2)
        set = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="channelWlan1"]/option[2]')))
        set.click()
        time.sleep(5)
        apply = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="applyWs"]')))
        apply.click()
        time.sleep(5)
        ok = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[54]/div[7]/div/button')))
        ok.click()
        time.sleep(10)
        okay = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[54]/div[7]')))
        okay.click()

        time.sleep(20)



    except:
        browser.quit()



if __name__ == '__main__':
    main()
