from mysql import connector
import time
import vaderSentiment.vaderSentiment as vader
import schedule
import re
from nltk.tokenize import sent_tokenize
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import PIL.Image as image

# host = "chinaaseanocean.mysql.rds.aliyuncs.com"  # 服务器
# root = "E:\\tomcat\\webapps\\sentiment_img"  # 服务器
host = "chinaasean.mysql.rds.aliyuncs.com"  # 本地测试
root = os.getcwd()  # 本地测试


def main():
    try:
        date = time.strftime('%Y-%m-%d', time.localtime())
        # date = '2019-07-16'
        conn = connector.connect(host=host, database="chinaaseanocean",
                                 user="chinaaseanocean", password="x3m0u8X#M)U*")
        news = get_today_news(date, conn)
        filter_en_news(news)
        if len(news) != 0:
            create_dir(date)
            senti_analysis(news, date)
            gene_word_cloud(news, date)
            insert_path(date, conn)
        conn.disconnect()
    except Exception as e:
        print(e)


def create_dir(date):
    """  创建与日期对应的文件夹 """
    path = root + os.sep + date
    if not os.path.exists(path):
        os.mkdir(path)


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""

    if '\u4e00' <= uchar <= '\u9fff':
        return True

    else:
        return False


def get_today_news(date, conn):
    """   获得今天的新闻  """
    cursor = conn.cursor()
    sql = "SELECT country_name, title, content FROM sea_news WHERE crawled_time LIKE '%" + date + "%'"
    cursor.execute(sql)
    news = cursor.fetchall()
    cursor.close()
    news = [list(x) for x in news]
    return news


def filter_en_news(news):
    """  筛选英文新闻  """
    pat = re.compile('<[^>]*>')
    for i in range(len(news))[::-1]:
        # 如果这条新闻没有任何内容，删除ε=( o｀ω′)ノ
        text = pat.sub('', str(news[i][2])).strip().replace('\n', '')
        news[i][2] = sent_tokenize(text)
        if not news[i][2]:
            news.pop(i)
            continue
        # 如果新闻标题含有汉字，删除ε=( o｀ω′)ノ
        for char in news[i][1]:
            if is_chinese(char):
                news.pop(i)
                break


def senti_analysis(news, date):
    """
    对新闻进行情感分析
    每个句子会得到积极分、消极分、中性分、综合分，句子的平均得分为新闻整体得分
    分析图表路径存在数据库中
    """
    analyzer = vader.SentimentIntensityAnalyzer()
    all_sentiment = pd.DataFrame(columns=('Positive', 'Negative', 'Neutral', 'Compound'))
    for article in news:
        article_pos = 0
        article_neg = 0
        article_neu = 0
        article_compo = 0
        for sent in article[2]:
            score = analyzer.polarity_scores(sent)
            article_pos += score['pos']
            article_neg += score['neg']
            article_neu += score['neu']
            article_compo += score['compound']
        length = len(article[2])
        article_sentiment = pd.DataFrame([[article_pos / length, article_neg / length, article_neu / length,
                                           article_compo / length]],
                                         columns=('Positive', 'Negative', 'Neutral', 'Compound'))
        all_sentiment = all_sentiment.append(article_sentiment)
    all_sentiment.reset_index(drop=True, inplace=True)
    country = [x[0] for x in news]
    # 不加plt.close()会产生图片覆盖
    img1 = sns.boxplot(y=all_sentiment['Positive'], x=country)
    # plt.show()
    plt.close()
    img2 = sns.boxplot(y=all_sentiment['Negative'], x=country)
    # plt.show()
    plt.close()
    img3 = sns.boxplot(y=all_sentiment['Neutral'], x=country)
    # plt.show()
    plt .close()
    img4 = sns.boxplot(y=all_sentiment['Compound'], x=country)
    # plt.show()
    plt.close()
    img1.figure.savefig(root + os.sep + date + os.sep + "img1.png")
    img2.figure.savefig(root + os.sep + date + os.sep + "img2.png")
    img3.figure.savefig(root + os.sep + date + os.sep + "img3.png")
    img4.figure.savefig(root + os.sep + date + os.sep + "img4.png")


def gene_word_cloud(news, date):
    text = ''
    for article in news:
        for sent in article[2]:
            text = text + sent
    stop_words = set(STOPWORDS)
    stop_list = ["said", "will"]
    for word in stop_list:
        stop_words.add(word)
    mask = np.array(image.open('template.jpg'))
    # word_cloud = WordCloud(background_color="white", height=860, width=1000, stopwords=stop_words).generate(text)
    word_cloud = WordCloud(mask=mask, stopwords=stop_words, height=500, width=1000).generate(text)
    word_cloud.to_file(root + os.sep + date + os.sep + "img5.png")


def insert_path(date, conn):
    """  把图片路径插入数据库 """
    cursor = conn.cursor()
    path = "http://chinaaseanocean.cn/sentiment_img/" + date + "/" + "img"
    sql = "REPLACE INTO `senti_img`(code, date, path) VALUES (%s, %s, %s)"
    for i in range(1, 6):
        cursor.execute(sql, (i, date, path + str(i) + ".png"))
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    main()
    schedule.every(5).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
