# coding: UTF-8
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

import logging
from logging import getLogger, StreamHandler, Formatter
import os
import sys
import traceback

import random

import message

logger = getLogger("LogToukare")
logger.setLevel(logging.DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(logging.INFO)
handler_format = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(handler_format)

handler2 = logging.FileHandler(filename="toukare.log")  #handler2はファイル出力
handler2.setLevel(logging.DEBUG)     #handler2はLevel.WARN以上
handler2.setFormatter(logging.Formatter("%(asctime)s %(levelname)8s %(message)s"))

logger.addHandler(stream_handler)
logger.addHandler(handler2)



# RANDOM_STA = 1
# RANDOM_END = 5

def readSettings(param):
    return os.environ.get(param)

def saveScreenshot(browser,name):
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), name +".png")
    browser.save_screenshot(FILENAME)
    message.sendScreenShot2Discord(browser,
        name,
        readSettings('DISCORD_WEBHOOK'))

def moveListPage(browser):
    try:
        browser.get('https://tokyo-calendar-date.jp/search/list/0')
    except Exception as e:
        logger.info('something error occourd in moveListPage.')
        logger.debug(traceback.format_exc())
        browser.get('https://tokyo-calendar-date.jp/search/list/0')
        message.sendScreenShot2Discord(browser,
        'Something error occored in moveListPage.',
        readSettings('DISCORD_WEBHOOK'))

def once_foot(browser):
    cnt = 0
    err_flg = False
    logger.info("start once_foot.")

    for i in range(4,9):
        moveListPage(browser)
        for j in range(2,250):
            # r1 =  random.randint(RANDOM_STA,RANDOM_END)
            # r2 =  random.randint(RANDOM_STA,RANDOM_END)
            cnt += 1
            if(cnt > 40):
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight+100);")
                cnt = 0

            try:
                if j % 25 == 0:
                    logger.info("i:{} j:{}".format(i,j))
                e = browser.find_element_by_xpath('//*[@id="matchableUsers"]/div[' + str(j) + ']/div/a/div[1]/div')
                e.click()
            except Exception as e:
                try:
                    e = browser.find_element_by_xpath('//*[@id="matchableUsers"]/div[' + str(j) + ']/div/a/div[1]/div')
                    e.click()
                except Exception as e:
                    logger.info('something error occourd in once_foot.i:{} j:{}'.format(i,j))
                    message.sendScreenShot2Discord(browser,
                        'Something error occored in once_foot.',
                        readSettings('DISCORD_WEBHOOK'))
            # time.sleep(r1)
            toukare_like(browser)
            toukare_back(browser)
            # time.sleep(r2)
        else:
            cnt = 0

        
    #browser.refresh()
    moveListPage(browser)

def toukare_like(browser):
    xpath = '//*[@id="user_buttons"]/div/a'

    try:
        e = browser.find_element_by_xpath(xpath)
        e.click()
    except Exception as e:
        try:
            e = browser.find_element_by_xpath(xpath)
            e.click()
        except Exception as e:
            logger.info('something error occourd in toukare_like.')
            logger.debug(traceback.format_exc())
            message.sendScreenShot2Discord(browser,
                'Something error occored in toukare_like.',
                readSettings('DISCORD_WEBHOOK'))

def toukare_back(browser):
    xpath = '//*[@id="userProfile"]/div[4]/div[2]/a'
    try:
        e = browser.find_element_by_xpath(xpath)
        e.click()
    except Exception as e:
        try:
            e = browser.find_element_by_xpath(xpath)
            e.click()
        except Exception as e:
            logger.info('something error occourd in toukare_back.')
            logger.debug(traceback.format_exc())
            message.sendScreenShot2Discord(browser,
                'Something error occored in toukare_back.',
                readSettings('DISCORD_WEBHOOK'))

def toukare_point(browser):
    xpath_menu = '//*[@id="mainContent"]/div[1]/div[2]/a'
    vote_url = 'https://tokyo-calendar-date.jp/vote'
    xpath_OK = '//*[@id="voteOK"]'
    source = None
    try:
        browser.get(vote_url)
    except UnexpectedAlertPresentException:
        alert = browser.switch_to_alert()
        alert.accept()
    except Exception as e:
        logger.info('Error occourd in toukare_point at request VOTE_URL.')
        logger.debug(traceback.format_exc())
        saveScreenshot(browser,traceback.format_exc())
    try:
        #指定したdriverに対して最大で30秒間待つように設定する
        wait = WebDriverWait(browser, 30)
        #指定された要素(検索テキストボックス)が表示状態になるまで待機する
        element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH,xpath_OK)))
    except Exception as e:
        logger.debug(traceback.format_exc())
        saveScreenshot(browser,traceback.format_exc())
        return

    saveScreenshot(browser, "point1")

    for i in range(int(readSettings('TOUKARE_POINT'))):
        try:
            e = browser.find_element_by_xpath('//*[@id="voteOK_wrap"]')
            e.click()
            source = browser.page_source
        except Exception as e:
            try:
                e = browser.find_element_by_xpath(xpath_OK)
                e.click()
            except Exception as e:
                logger.info('something error occourd in toukare_point.')
                logger.debug(traceback.format_exc())
                message.sendScreenShot2Discord(browser,
                    'Something error occored in toukare_point.',
                    readSettings('DISCORD_WEBHOOK'))
                break
        def compare_source(browser):
            try:
                return source != browser.page_source
            except Exception:
                pass
        WebDriverWait(browser, 10).until(compare_source)

def init():
    global COOKIES
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-gpu')
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--window-size=300x500')
    chromeOptions.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1')    
    chromeOptions.add_argument('--disable-dev-shm-usage')
    chromeOptions.add_argument('--disable-extensions');
    chromeOptions.add_argument('--proxy-server="direct://"');
    chromeOptions.add_argument('--proxy-bypass-list=*');
    browser = webdriver.Chrome(chrome_options=chromeOptions)
    browser.set_window_size(400,800)
    moveListPage(browser)
    #要素がロードされるまでの待ち時間を10秒に設定
    browser.implicitly_wait(10)

    # 位置情報の設定を許可（許可をしないと位置情報の設定ができない）
    browser.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://tokyo-calendar-date.jp",
            "permissions": ["geolocation"]
        },
    )

    # 緯度、経度、緯度・経度の誤差(単位：m)を設定する
    browser.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": 35.689487,
            "longitude": 139.691706,
            "accuracy": 100,
        },
    )

    return browser

def fbLoginWith(browser):    
    # FBへ遷移
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/a[1]').click()
    saveScreenshot(browser,"fb1")
    browser.find_element_by_xpath('/html/body/div[4]/a[1]').click()
    saveScreenshot(browser,"fb2")
    # ウインドウを最後に切り替える
    browser.switch_to.window(browser.window_handles[-1])
    saveScreenshot(browser,"fb3")
    # idInput = browser.find_element_by_xpath('//*[@id="m_login_email"]').send_keys(readSettings('MAIL'))
    # passInput = browser.find_element_by_xpath('//*[@id="m_login_password"]').send_keys(readSettings('PASS'))
    browser.execute_script(
        'document.getElementById("m_login_email").value="{}";'.format(readSettings('MAIL'))
    )
    browser.execute_script(
        'document.getElementById("m_login_password").value="{}";'.format(readSettings('PASS'))
    )

    browser.find_element_by_xpath('//*[@id="u_0_4"]/button').click()
    # saveScreenshot(browser,"fb4")
    browser.switch_to.window(browser.window_handles[0])
    saveScreenshot(browser,"fb5")

    #FB側でおかしいので追加
    #browser.find_element_by_xpath('//*[@id="u_0_1"]').click()

    time.sleep(10)
    return

def toukare_sujest(browser):
    xpath_go = '//*[@id="mainContent"]/div[1]/div[3]/a'
    xpath_start = '//*[@id="playBtnOn"]/a'
    xpath_OK = '//*[@id="playWrap"]/div[2]/div/div/div[2]/a'

    moveListPage(browser)

    try:
        e = browser.find_element_by_xpath(xpath_go).click()
        e = browser.find_element_by_xpath(xpath_start).click()
    except Exception as e:
        try:
            e = browser.find_element_by_xpath(xpath_go).click()
            e = browser.find_element_by_xpath(xpath_start).click()
        except Exception as e:
            logger.info('something error occourd in toukare_sujest.')
            logger.debug(traceback.format_exc())

    for i in range(15):
        try:
            e = browser.find_element_by_xpath(xpath_OK)
            e.click()
        except Exception as e:
            try:
                e = browser.find_element_by_xpath(xpath_OK)
                e.click()
            except Exception as e:
                logger.info('something error occourd in toukare_sujest.')
                logger.debug(traceback.format_exc())
    moveListPage(browser)
    return

if __name__ == '__main__':

    browser = init()
    message.lineapi("toukare.py start.")
    fbLoginWith(browser)
    toukare_point(browser)
    for i in range(int(readSettings('TOUKARE_MAX_LIKE'))):
        once_foot(browser)
        moveListPage(browser)
    browser.close()
    message.lineapi("toukare.py end.")
    logger.info('プログラム終了')
    sys.exit()
