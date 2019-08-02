import re
import time
from warnings import filterwarnings
from pyquery import PyQuery
from pymysql import connect
from pymysql.err import OperationalError
from urllib3.connectionpool import InsecureRequestWarning
from newspaper import Article, ArticleException
from datetime import timedelta, datetime


class NewsCrawler(object):

    # ---------------------------------------数据库配置--------------------------------------- #

    user = 'chinaaseanocean'
    password = 'x3m0u8X#M)U*'
    port = 3306
    db = 'chinaaseanocean'
    host = "chinaasean.mysql.rds.aliyuncs.com"  # 本地测试
    # host = "chinaaseanocean.mysql.rds.aliyuncs.com"  # 服务器

    # ----------------------------------------参数配置---------------------------------------- #

    country, category, base_url, query, date_format = None, None, None, None, None

    verify = False     # 是否关闭https验证，默认关闭

    only_today = True  # 默认只爬取今天新闻

    show_error = True  # 默认显示错误信息

    tag = 'href'       # 默认用href属性提取url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.131 Safari/537.36'
    }

    page_format = '?max_page='

    max_page = 10000  # 默认数值很大（爬完全部）

    test = False  # 开启测试会输出url title date 信息，并把信息插入测试数据库asean_news_test

    # ----------------------------------------配置结束---------------------------------------- #

    filterwarnings('ignore', category=InsecureRequestWarning)  # 忽略https警告

    def __init__(self):
        self.items = [self.country, self.base_url]
        self.stop_yield = False
        if self.only_today:
            self.today = time.strftime('%Y-%m-%d', time.localtime())
        self._mysql_connect()

    @staticmethod
    def _get_yesterday():
        _yesterday = datetime.today() + timedelta(-1)
        yesterday = _yesterday.strftime('%Y-%m-%d')
        return yesterday

    def _mysql_connect(self):
        while True:
            try:
                self.conn = connect(host=NewsCrawler.host, user=NewsCrawler.user, password=NewsCrawler.password,
                                    port=NewsCrawler.port, db=NewsCrawler.db)
            except OperationalError as e:
                if self.show_error:
                    print('\r正在重新连接数据库.... 原因:', e, end='', flush=True)
                time.sleep(1)
            else:
                break

    # noinspection DuplicatedCode
    def start_url(self):
        """
        遍历分类字典，生成url请求
        可重写此方法
        """
        for class_1 in self.category.keys():
            self.items.append(class_1)
            if self.category[class_1]:
                for class_2 in self.category[class_1]:
                    self.items.append(class_2)
                    url = self.base_url + '/' + class_2
                    for i in range(self.max_page + 1):
                        if self.stop_yield:
                            self.stop_yield = False
                            break
                        yield url + self.page_format + str(i)
                    self.items[3:] = []
            else:
                self.items.append(None)
                url = self.base_url + '/' + class_1
                for i in range(self.max_page + 1):
                    if self.stop_yield:
                        self.stop_yield = False
                        break
                    yield url + self.page_format + str(i)
                self.items[3:] = []
            self.items[2:] = []

    def get_links(self, url):
        """  获取所生成的url页面上的新闻链接  """
        failure = 0
        while failure < 3:
            try:
                if self.test:
                    print(url)
                doc = PyQuery(url, headers=self.headers, verify=self.verify)
            except Exception as e:
                failure += 1
                if self.show_error:
                    print('\r' + self.base_url + '获取新闻链接失败，原因：', e, end='', flush=True)
            else:
                links = [link.attr(self.tag) for link in doc(self.query).items()]
                if len(links) == 0:
                    self.stop_yield = True
                return links
        else:
            return []

    def process_links(self, links):
        """  使用newspaper库提取新闻正文要素入库, newspaper无效则重写此方法  """
        for link in links:
            if self.base_url not in link:
                link = self.base_url + link
            article = Article(link)
            failure = 0
            while failure < 3:
                try:
                    article.download()
                    article.parse()
                except ArticleException as e:
                    if self.show_error:
                        print('\r' + self.base_url + '新闻解析出错，原因：', e)
                    failure += 1
                else:
                    date = self.get_date(article)
                    if self.only_today:
                        if date != self.today and date is not None:
                            self.stop_yield = True
                            break
                    if self.test:
                        print(article.url)
                        print(date)
                    if article.text:
                        self.items.extend([article.title, date, article.text, article.url])
                        self._insert_data()
                    break
            else:
                continue

    def get_date(self, article):
        """
        正则表达式匹配日期
        """
        date = article.publish_date
        if not date:
            for i, regex in enumerate(self.date_format[0]):
                try:
                    pattern = re.compile(regex)
                    date = pattern.findall(article.html)[0]
                except IndexError:
                    continue
                else:
                    try:
                        date = time.strptime(date, self.date_format[1][i])
                        date = time.strftime('%Y-%m-%d', date)
                    except ValueError:
                        pass
        return date

    def _insert_data(self):
        cursor = self.conn.cursor()
        if self.test:
            sql = 'REPLACE INTO `asean_news_test`(country, domain, class_1, class_2, title, publish_date, content,' \
                  ' url) VALUES (%s)' % (','.join(['%s'] * 8))
        else:
            sql = 'REPLACE INTO `asean_news`(country, domain, class_1, class_2, title, publish_date, content, url)' \
                  ' VALUES (%s)' % (','.join(['%s'] * 8))
        cursor.execute(sql, tuple(self.items))
        # print('yes')
        self.conn.commit()
        cursor.close()
        self.items[4:] = []

    @classmethod
    def _get_crawler(cls):
        return cls()

    @classmethod
    def run(cls):

        crawler = cls._get_crawler()

        begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('\n', crawler.base_url, begin, 'BEGIN', flush=True)

        for url in crawler.start_url():
            links = crawler.get_links(url)
            if len(links) == 0:
                continue
            crawler.process_links(links)

        end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('\n', crawler.base_url, end, 'DONE', flush=True)

        crawler.conn.close()

    __author__ = 'sxy'

