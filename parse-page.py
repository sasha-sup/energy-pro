import os
import re
import sys
import time
import logging
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from googletrans import Translator


url = 'https://my.energo-pro.ge/ow/#/disconns'
xpath = '/html/body/app-root/app-disconns/main/div/div/div/div/div/div/div[2]/div/div[2]/div/'

# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename='e-pro.log',
                    filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")


# Check my.energo-pro.ge 
def check_page():
    response = requests.get(url)
    if response.status_code != 200:
        na_err = '❌ my.energo-pro.ge unavailable.'
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

def prepare_alert_mesage(alert_text):

# regex to remove html tags
    remove_html_tags = re.compile('<.*?>')
# translte message 
    translator = Translator()
    translated = translator.translate(alert_text, src='ka', dest='en')
    translated_alert_text=translated.text
# Remove tags with regex
    split_transleted_alert_text = re.split((remove_html_tags), translated_alert_text)
# Format string in to json
    jsonStr = json.dumps([x for x in split_transleted_alert_text if x])
    json_object = json.loads(jsonStr)
    json_formatted_str = json.dumps(json_object, indent=2)

    return json_formatted_str


def parse_page_selenium():

# Open url
    e_pro = set_up_driver()
    e_pro.maximize_window()
    e_pro.get(url)
    logging.info('✅ my.energo-pro.ge ready.')
    WebDriverWait(e_pro, 5).until(EC.presence_of_element_located((By.XPATH, xpath+'form/div/div/div/div')))
    e_pro.find_element(By.XPATH, xpath+'form/div/div/div/div').click()
    time.sleep(1)
    e_pro.find_element(By.XPATH, xpath+'form/div/div/div/div/div/div/ul/li[9]').click()
    #9 batumi
    logging.info('✅ Target city found.')

    if e_pro.find_element(By.XPATH, xpath+'div[1]').is_displayed():
        error_mes = '❌ Target city\'s list is empty.'
        logging.error(error_mes)
        e_pro.close()
        return(error_mes)
    else:
        logging.info('✅ Target city has announcement.')
        element_found = '✅ Element found.'
        element_not_found = '❌ Element not found.'


        if e_pro.find_element(By.XPATH, xpath+'div[2]/div').is_displayed():
            logging.info(element_found)
            e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[1]/div[1]/div[3]/div[1]').click()
            alert_text=(WebDriverWait(e_pro, 20).until(EC.visibility_of_element_located((By.XPATH, xpath+'div[2]/div/div[1]/div[2]/div/div'))).get_attribute("innerHTML"))
            print(prepare_alert_mesage(alert_text))

            time.sleep(1)
        try: 
            if e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[2]/div[1]/div[4]/div/div[1]').is_displayed():
                logging.info(element_found)
                e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[2]/div[1]/div[4]/div/div[1]').click()
                time.sleep(1)
            else:
                logging.error(element_not_found)

            if e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[3]/div[1]/div[4]/div/div[1]/div[1]').is_displayed():
                logging.info(element_found)
                e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[3]/div[1]/div[4]/div/div[1]/div[1]').click()
                time.sleep(1)
            else:
                logging.error(element_not_found)

            if e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[4]/div[1]/div[4]/div/div[1]').is_displayed():
                logging.info(element_found)
                e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[4]/div[1]/div[4]/div/div[1]').click()
            else:
                logging.error(element_not_found)

            if e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[5]/div[1]/div[4]/div/div[1]/div[1]').is_displayed():
                logging.info(element_found )
                e_pro.find_element(By.XPATH, xpath+'div[2]/div/div[5]/div[1]/div[4]/div/div[1]/div[1]').click()
            else:
                logging.error(element_not_found)
        except:
            logging.error(element_not_found)
            pass



        time.sleep(666)


if __name__ == '__main__':
    check_page()
    parse_page_selenium()