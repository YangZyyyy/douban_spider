from time import sleep
from typing import Mapping

from bs4.element import Comment
from utils import get_html
from tqdm import tqdm
from bs4 import BeautifulSoup
from utils import *
import pandas as pd



cookie = 'bid=ylJygUgJw7M; gr_user_id=c7608709-7ae7-4aa6-96a2-2cb42b5763f5; _vwo_uuid_v2=D06FB660D1BB9DA258CEF1DD05E13915C|2f98c2a462a7d99782bda6e6bdebbe2d; viewed="4033983_26323699"; ll="118371"; __utmv=30149280.22731; douban-profile-remind=1; __yadk_uid=pse43jF08ndeEe9KtJxJ9Q033gWmTKLH; douban-fav-remind=1; __utmz=30149280.1625674193.14.8.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided); dbcl2="227311352:Ivr8EZrweHQ"; push_noty_num=0; push_doumail_num=0; __gads=ID=364fee243a0f8f72-22c68d7d6eca007f:T=1626737837:RT=1626737837:S=ALNI_MYFvzTisDBHAoFN5iw1Hk5Iu0rrbg; ck=TTKz; _pk_ref.100001.8cb4=["","",1626958688,"https://www.google.com/"]; _pk_id.100001.8cb4=ea216afe0cc5f88c.1610268976.15.1626958688.1626931173.; _pk_ses.100001.8cb4=*; ap_v=0,6.0; __utma=30149280.583283763.1610108536.1626791427.1626958688.17; __utmc=30149280; __utmt=1; __utmb=30149280.3.9.1626958688'
sleep_time = 2

def list_spider(url):
    '''
    用来爬豆瓣小组列表页面，如
    https://www.douban.com/group/469687/discussion?start=0

    return:
    discuss_tittle, author, reply_num, last_reply_date, title_href, name_href
    '''
    discuss_tittle, author, reply_num, last_reply_date, title_href, author_id = [], [], [], [], [], []
    html = get_html(url, cookie, sleep_time)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find_all('tr')
    for i in range(1, len(table)):
        tds = table[i].find_all('td')
        discuss_tittle.append(tds[0].a.string.replace(' ', '').replace('\n', ''))
        title_href.append(tds[0].a['href'])
        author.append(tds[1].a.string)
        author_id.append(tds[1].a['href'].split('/')[-2])
        reply_num.append(tds[2].string)
        last_reply_date.append(tds[3].string)
    
    return discuss_tittle, author,author_id,reply_num, last_reply_date, title_href

def article_spider(url):
    '''
    用来爬豆瓣小组帖子页面，如
    https://www.douban.com/group/topic/228874095/

    return:
    title, name, name_id, date, article, comments(name, id, date, content)
    '''
    comments = {
        'id':[],
        'name':[],
        'date':[],
        'content':[]
    }
    html = get_html(url, cookie, sleep_time)
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(class_='article').h1.string.replace(' ','').replace('\n', '')
    name = soup.find(class_='from').a.string
    name_id = soup.find(class_='from').a['href'].split('/')[-2]
    date = soup.find(class_='create-time color-green').string
    article = ''
    lines = soup.find(class_='rich-content topic-richtext').find_all('p')
    for line in lines:
        if line.string:
            article += (line.string + '\n')
    
    replications = soup.find(id='popular-comments').find_all('li')
    for li in replications:
        comments['id'].append(li['data-author-id'])
        comments['name'].append(li.find(class_='bg-img-green').h4.a.string)
        comments['date'].append(li.find(class_='bg-img-green').find(class_='pubtime').string)
        comments['content'].append(li.find(class_='reply-content').string)
    
    return title, name, name_id, date, article, comments


if __name__ == '__main__':
    # discuss_tittle, author, author_id, reply_num, last_reply_date, title_href = list_spider('https://www.douban.com/group/469687/discussion?start=0')
    # pd.DataFrame({
    #     'title':discuss_tittle,
    #     'author':author,
    #     'author_id':author_id,
    #     'reply_num':reply_num,
    #     'last_reply_date':last_reply_date,
    #     'title_href':title_href,
    # }).to_csv('list.csv', index=False)
    
    res = article_spider('https://www.douban.com/group/topic/228874095/')
    print(res)