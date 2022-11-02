import os
import re
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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


# Setup WebDriver Chrome
def set_up_driver():
    options = Options()
    prefs = {
        "translate_whitelists": {"ge":"en"},
        "translate":{"enabled":"true"}
    }
    options.add_experimental_option("prefs", prefs)
    web = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    logging.info('✅ Driver init.')
    return(web)


# Import project name
def import_project_name():

# Open url
    e_pro = set_up_driver()
    e_pro.maximize_window()
    e_pro.get(url)
    logging.info('✅ URL Ready.')
    WebDriverWait(e_pro, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div')))
    e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div').click()
    time.sleep(1)
    e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/form/div/div/div/div/div/div/ul/li[9]').click()
    logging.info('✅ Target city found.')
    if e_pro.find_element(By.XPATH, '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/div[1]').is_displayed():
        logging.error('❌ Target city\'s list is empty.')
    else:
        logging.info('✅ Target city has announcement.')


    time.sleep(666)


if __name__ == '__main__':
    import_project_name()