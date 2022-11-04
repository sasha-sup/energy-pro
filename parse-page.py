import os
import re
import sys
import time
import logging
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime



url = "https://my.energo-pro.ge/ow/#/disconns"


# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename='e-pro.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")


# Check my.energo-pro.ge 
def check_page():
    response = requests.get(url)
    if response.status_code != 200:
        na_err = '😬 my.energo-pro.ge unavailable.'
        logging.info(na_err)
        return(na_err)
    else:
        pass
        logging.info('✅ my.energo-pro.ge available.')
        

# Setup WebDriver Chrome
def set_up_driver():
    web = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    logging.info('✅ Driver init.')
    return(web)


def parse_page_selenium():

# Open url
    e_pro = set_up_driver()
    e_pro.maximize_window()
    e_pro.get(url)
    logging.info('✅ my.energo-pro.ge ready.')
    WebDriverWait(e_pro, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div')))
    e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div').click()
    time.sleep(1)
    e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div/div/div/ul/li[1]').click()
    #9
    logging.info('✅ Target city found.')
    if e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]').is_displayed():
        error_mes = '❌ Target city\'s list is empty.'
        logging.error(error_mes)
        e_pro.close()
        return(error_mes)
    else:
        if e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div').is_displayed():
            parentElement = e_pro.find_element(By.CLASS_NAME, 'page-alerts-content-wrap')
            elementList = parentElement.find_elements(By.CLASS_NAME, 'page-alert-wrap ng-star-inserted')
            print(elementList) 
            time.sleep(666)
            logging.info('✅ Target city has announcement.')







    


if __name__ == '__main__':
    check_page()
    parse_page_selenium()