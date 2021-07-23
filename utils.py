import requests
import time
import random

def get_html(url, cookie, sleep_time=2):
    '''
    通过Url获取html文本内容，
    参数：
    sleep_time 每次爬取网页暂停的时长
    cookie
    '''
    s = requests.session()
    time.sleep(random.random() * sleep_time)
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Cookie':cookie
    }
    return s.get(url, headers=headers).text

