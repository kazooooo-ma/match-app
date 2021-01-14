# coding: UTF-8
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import logging
from logging import getLogger, StreamHandler, Formatter
import os
import sys
import traceback

import re
import random
import message

logger = getLogger("LogWith")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

handler2 = logging.FileHandler(filename="with.log")  #handler2はファイル出力
handler2.setLevel(logging.DEBUG)     #handler2はLevel.WARN以上
handler2.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))

logger.addHandler(stream_handler)
logger.addHandler(handler2)


# RANDOM_STA = 1
# RANDOM_END = 5

def readSettings(param):
    return os.environ.get(param)

def once_foot(browser):
    cnt = 0
    err_flg = False
    i = 5
    logger.info("start once_foot.")
    for iNew in range(4,9):
        for j in range(1,60):
            # r1 =  random.randint(RANDOM_STA,RANDOM_END)
            # r2 =  random.randint(RANDOM_STA,RANDOM_END)
            cnt += 1

            try:
                e = browser.find_element_by_xpath('/html/body/div[5]/div[4]/div['+ str(i) +']/div/div[1]/div['+ str(j) +']/a/div/img[1]')
                e.click()
            except Exception as e:
                try:
                    e = browser.find_element_by_xpath('/html/body/div[5]/div[4]/div['+ str(i) +']/div/div[1]/div['+ str(j) +']/a/div/img')
                    e.click()
                except Exception as e:
                    logger.info('something error occourd in once_foot.i:{} j:{}'.format(i,j))
                    err_flg = True
                    continue
            # time.sleep(r1)

            #browser.back()
            browser.get("https://with.is/search")
            # time.sleep(r2)

            err_flg = False
        else:
            cnt = 0

        
    browser.refresh()

def once_foot2(browser,page):
    cnt = 0
    err_flg = False
    i = 0
    if page == 1:
        i = 5
    else:
        i = 6

    URL = 'https://with.is/search?page={}&paging_order=0'.format(page)
    logger.info("start once_foot. url={}".format(URL))

    browser.get(URL)
    time.sleep(10)

    for j in range(1,60):
        # r1 =  random.randint(RANDOM_STA,RANDOM_END)
        # r2 =  random.randint(RANDOM_STA,RANDOM_END)
        try:
            e = browser.find_element_by_xpath('/html/body/div[5]/div[4]/div['+ str(i) +']/div/div[1]/div['+ str(j) +']/a/div/img[1]')
            e.click()
        except Exception as e:
            try:
                e = browser.find_element_by_xpath('/html/body/div[5]/div[4]/div['+ str(i) +']/div/div[1]/div['+ str(j) +']/a/div/img')
                e.click()
            except Exception as e:
                logger.info('something error occourd in once_foot.i:{} j:{}'.format(i,j))
                err_flg = True
                continue
        # time.sleep(r1)

        #browser.back()
        browser.get(URL)
        # time.sleep(r2)
    browser.refresh()


def init_with():
    global COOKIES
    url = "https://with.is/welcome"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--window-size=400x800')
    #chromeOptions.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1')
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.set_window_size(1280,1280)
    browser.implicitly_wait(10)
    browser.get(url)
    return browser

def fbLoginWith(browser):    
    # ログイン（右上）
    xpath = '/html/body/div[1]/div[1]/div[1]'

    wait = WebDriverWait(browser, 10)
    element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))

    element.click()
    # FBへ遷移
    browser.find_element_by_xpath('//*[@id="login"]/div[3]/a/img').click()
    idInput = browser.find_element_by_id('email').send_keys(readSettings('MAIL'))
    passInput = browser.find_element_by_id('pass').send_keys(readSettings('PASS'))
    browser.find_element_by_xpath('//*[@id="loginbutton"]').click()
    return

def getSearchNum(browser):
    try:
        num = browser.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div/div[2]/span').text
        num = re.sub("\\D", "", num)

        logger.debug('検索結果数は、{}人です。'.format(num))
    except Exception as e:
        logger.error(traceback.format_exc())
        num = 300

    return num


if __name__ == '__main__':
    message.lineapi('with.py start.')
    browser = init_with()

    fbLoginWith(browser)

    getSearchNum(browser)
    maxcnt = int(readSettings('WITH_MAX'))

    c = 1
    while(c * 60 < int(maxcnt)):
        once_foot2(browser, c)
        c += 1
    browser.get('https://with.is/search')
    browser.close()
    message.lineapi('with.py end.')
    logger.info('プログラム終了')
    sys.exit()

