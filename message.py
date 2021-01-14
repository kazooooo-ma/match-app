import requests
import os
from discordwebhook import Discord

def readSettings(param):
    return os.environ.get(param)

def lineapi(message):
    if(readSettings('LINE_ENABLE') and readSettings('LINE_TOKEN') != None):
        url = "https://notify-api.line.me/api/notify"
        token = readSettings('LINE_TOKEN')
        headers = {"Authorization" : "Bearer "+ token}
        #message =  "hey!!"
        payload = {"message" :  message}
        #files = {"imageFile": open("test.jpg", "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。
        r = requests.post(url ,headers = headers ,params=payload)
        return r

def sendScreenShot2Discord(browser, message, url):
    FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screen.png")
    browser.save_screenshot(FILENAME)
    discord = Discord(url=url)
    with open(FILENAME, 'rb') as f:
        discord.post(content=message , file={ "attachment": f })

if __name__ == '__main__':
    print(readSettings('LINE_TOKEN'))