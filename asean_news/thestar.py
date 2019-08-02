import time
from newspaper.article import Article
from pymysql import connect
from pymysql import OperationalError
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from newspaper.article import ArticleException
import requests
from warnings import filterwarnings
from urllib3.connectionpool import InsecureRequestWarning

"""
用于爬取www.thestar.com.my网站的新闻，该网站属于马来西亚
"""


categories = ['Nation', 'Business', 'Education', 'Regional', 'World', 'Metro', 'Tech', 'Lifestyle']
# host = "chinaaseanocean.mysql.rds.aliyuncs.com"  # 服务器
host = "chinaasean.mysql.rds.aliyuncs.com"  # 本地测试
MAX_PAGE = 25  # 此网站似乎最多回溯25页
base_url = 'https://www.thestar.com.my/news/latest/?'
domain = 'www.thestar.com.my'
params = {}.fromkeys(['tag', 'pgno'])
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.131 Safari/537.36'
}
filterwarnings('ignore', category=InsecureRequestWarning)


def crawl_archive():
    """
    爬取过去一周的所有新闻
    """
    conn = connect(host=host, user='chinaaseanocean', password='x3m0u8X#M)U*', port=3306, db='chinaaseanocean')
    for c in categories:
        for i in range(1, MAX_PAGE + 1):
            params['tag'] = c
            params['pgno'] = str(i)
            page_url = base_url + urlencode(params)
            try:
                doc = pq(page_url, headers=headers, verify=False)
            except requests.exceptions.ConnectionError as e:
                print(e)
                doc = pq(page_url, headers=headers, verify=False)
            ul = doc('ul.timeline > li')
            for li in ul.items():
                url = li.find('h2 a').attr('href')
                article = Article(url)
                try:
                    article.download()
                    article.parse()
                except ArticleException as e:
                    print(e)
                    continue
                title = article.title
                date = article.publish_date
                content = article.text
                class_2 = li.find('div.timeline-content > a').text()
                if content:
                    print(title)
                    cursor = conn.cursor()
                    sql = 'REPLACE INTO `asean_news` VALUES (%s)' % (','.join(['%s'] * 9))
                    cursor.execute(sql, ('Malaysia', domain, c, class_2, None, title, date, content, url))
                    conn.commit()
                    cursor.close()
    conn.close()


def crawl_today():
    """   每天定时爬取, 5小时一次即可，每个类别爬取一页  """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('\n', domain, now, "BEGIN")
    while True:
        try:
            conn = connect(host=host, user='chinaaseanocean', password='x3m0u8X#M)U*', port=3306, db='chinaaseanocean')
        except OperationalError as e:
            print(e)
            time.sleep(3)
        else:
            break
    for class_1 in categories:
        params['tag'] = class_1
        params['pgno'] = str(1)
        page_url = base_url + urlencode(params)
        failure = 0
        while failure < 3:
            try:
                doc = pq(page_url, headers=headers, verify=False)
            except Exception as e:
                failure += 1
                print('\r获取新闻链接失败，原因：', e, end='', flush=True)
            else:
                break
        else:
            continue
        ul = doc('ul.timeline > li')
        for li in ul.items():
            url = li.find('h2 a').attr('href')
            article = Article(url)
            try:
                article.download()
                article.parse()
            except ArticleException as e:
                # print(e)
                continue
            content = article.text
            if content:
                title = article.title
                date = article.publish_date
                class_2 = li.find('div.timeline-content > a').text()
                # print(title)
                cursor = conn.cursor()
                sql = 'REPLACE INTO `asean_news` VALUES (%s)' % (','.join(['%s'] * 8))
                cursor.execute(sql, ('Malaysia', domain, class_1, class_2, title, date, content, url))
                conn.commit()
                cursor.close()
    conn.close()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('\n', domain, now, "DONE")


if __name__ == "__main__":
    crawl_today()
