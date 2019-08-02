import re
import time
from newspaper.article import Article
from pymysql import connect
from pymysql import OperationalError
from pyquery import PyQuery as pq
from newspaper.article import ArticleException

"""
用于爬取www.bernama.com网站上的新闻，该网站属于马来西亚
"""

domain = 'http://www.bernama.com'
class_ = {
    # 网页代号以及对应的分类
    'ge': 'general',
    'bu': 'business',
    'po': 'politics',
    'wn': 'world',
    'mtdc': 'mtdc'
}
# host = "chinaaseanocean.mysql.rds.aliyuncs.com"  # 服务器
host = "chinaasean.mysql.rds.aliyuncs.com"  # 本地测试
base_url = 'http://www.bernama.com/en/archive.php?'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.131 Safari/537.36'
}
pattern = re.compile(r'Last update: (../../....)')


def crawl_archive():
    """   爬取过去的新闻  """
    while True:
        try:
            conn = connect(host=host, user='chinaaseanocean', password='x3m0u8X#M)U*', port=3306, db='chinaaseanocean')
        except OperationalError:
            time.sleep(3)
        else:
            break
    for key in class_.keys():
        class_1 = class_[key]
        print(class_1)
        page = 1
        while True:
            page_url = base_url + key + '&max_page=' + str(page)
            print(page_url)
            failure = 0
            while failure < 3:
                try:
                    doc = pq(page_url, headers=headers, verify=False)
                except Exception as e:
                    failure += 1
                    print(e.with_traceback)
                else:
                    break
            else:
                continue
            a_list = doc('div.w3-justify a')
            if len(a_list) < 7:
                break
            for a in a_list.items():
                news_url = 'http://www.bernama.com/en/' + a.attr('href')
                article = Article(news_url)
                try:
                    article.download()
                    article.parse()
                except ArticleException as e:
                    print(e)
                    continue
                content = pattern.sub('', article.text).replace('\n', '')
                if content:
                    url = article.url
                    title = article.title
                    try:
                        date = '-'.join(pattern.findall(article.html)[0].split('/')[::-1])
                    except:
                        date = ''
                    print(title, date, content, sep='\n')
                    cursor = conn.cursor()
                    sql = 'REPLACE INTO `asean_news` VALUES (%s)' % (','.join(['%s'] * 9))
                    cursor.execute(sql, ('Malaysia', domain, class_1, None, None, title, date, content, url))
                    conn.commit()
                    cursor.close()
            page = page + 1
    conn.close()


def crawl_today():
    """
    用于每日更新
    """
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('\n', domain, now, "BEGIN", flush=True)
    while True:
        try:
            conn = connect(host=host, user='chinaaseanocean', password='x3m0u8X#M)U*', port=3306, db='chinaaseanocean')
        except OperationalError as e:
            print(e)
            time.sleep(3)
        else:
            break
    for key in class_.keys():
        class_1 = class_[key]
        # print(class_1)
        page = 1
        while page < 3:
            page_url = base_url + key + '&max_page=' + str(page)
            # print(page_url)
            failure = 0
            while failure < 3:
                try:
                    doc = pq(page_url, headers=headers, verify=False)
                except Exception as e:
                    failure += 1
                    print(e)
                else:
                    break
            else:
                continue
            a_list = doc('div.w3-justify a')
            for a in a_list.items():
                news_url = 'http://www.bernama.com/en/' + a.attr('href')
                article = Article(news_url)
                try:
                    article.download()
                    article.parse()
                except ArticleException as e:
                    print(e)
                    continue
                content = pattern.sub('', article.text).replace('\n', '')
                if content:
                    url = article.url
                    title = article.title
                    try:
                        date = '-'.join(pattern.findall(article.html)[0].split('/')[::-1])
                    except:
                        date = ''
                    # print(title, date, content, sep='\n')
                    cursor = conn.cursor()
                    sql = 'REPLACE INTO `asean_news` VALUES (%s)' % (','.join(['%s'] * 8))
                    cursor.execute(sql, ('Malaysia', domain, class_1, None, title, date, content, url))
                    conn.commit()
                    cursor.close()
            if len(a_list) < 7:
                break
            page = page + 1
    conn.close()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('\n', domain, now, "DONE")


if __name__ == '__main__':
    crawl_today()