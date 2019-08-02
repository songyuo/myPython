import selenium.webdriver
import requests
import re
import random
import sys
import newspaper
# r = requests.get('https://www.baidu.com/')
# print(r.status_code)
# print(r.headers)
# print(r.cookies)
# print(r.text)
# dd = {'a': 123}
# d = {'b': dd}
# print(d['b'])
# exit() if 21 < 55 else print(123)
# a = ['13', '456', '789']
# b = ['13215', '7897', '546']
# print(random.choice(a))
def fun1():
    url = 'https://www.thestar.com.my/news/nation/2019/07/25/federal-court-allows-appeal-over-decision-declaring-dap-reps-disqualification-as-unlawful/'
    article = newspaper.article.Article(url)
    article.download()
    article.parse()
    print(article.title, article.publish_date, article.tags, article.authors, article.text, sep='\n')


def fun2():
    url = 'https://www.thestar.com.my/news/latest/?tag=Nation'
    paper = newspaper.build(url)
    # paper2 = newspaper.build_article(url)
    print(paper.category_urls())
    for a in paper.articles:
        print(a)


fun1()

