import os
import urllib.parse
import subprocess as sp
from time import sleep
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger()
logger.setLevel(logging.INFO)

default_res = ('800', '600')
sp.getoutput('cp chromedriver /tmp/')
sp.getoutput('cp headless-chromium /tmp/')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=800x600')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.binary_location = '/tmp/headless-chromium'

driver = webdriver.Chrome(
    executable_path=os.path.abspath('/tmp/chromedriver'),
    options=chrome_options)


def lambda_handler(event, context):
    url = 'https://maritimedevcon.ca/'
    res = default_res
    nap = 1

    if 'queryStringParameters' in event:
        if 'res' in event['queryStringParameters']:
            res = event['queryStringParameters']['res'].split('x')

        if 'wait' in event['queryStringParameters']:
            nap = int(event['queryStringParameters']['wait'])

        if 'url' in event['queryStringParameters']:
            url = urllib.parse.unquote(event['queryStringParameters']['url'])
            if 'http' not in url:
                url = 'http://' + url
    try:
        driver.set_window_size(res[0], res[1])
        driver.get(url)
        sleep(nap)
        b64_screenshot = driver.get_screenshot_as_base64()
        return {
            'statusCode': 200,
            'body': b64_screenshot,
            'isBase64Encoded': True,
            'headers': {
                'Content-Type': 'image/png',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        print(f'Problem with headless chrome. url: {url}\n{e}')
        logger.exception(e)
        return {
            'statusCode': 500,
            'body': 'Something went wrong :(',
            'isBase64Encoded': False,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
