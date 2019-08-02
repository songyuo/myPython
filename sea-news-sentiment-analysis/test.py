import re
import vaderSentiment.vaderSentiment as vader
import pandas as pd
import numpy as np
from lxml.html.clean import Cleaner
from nltk.tokenize import sent_tokenize
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import time
import schedule
import mysql


def senti_score(date):
    df = pd.read_csv(date + "enNews.csv", sep=",")
    sentiment = pd.DataFrame(columns=('Positive', 'Negative', 'Neutral', 'Compound'))
    corpus = df.iloc[:, 8]
    pat = re.compile('<[^>]*>')
    analyzer = vader.SentimentIntensityAnalyzer()
    for html in corpus[:]:
        text = pat.sub('', html).strip().replace('\n', '')
        # with open("cloudText.txt", "a+", encoding='utf-8') as f:
        #     f.write(text)
        sent_list = sent_tokenize(text)
        article_pos = 0
        article_neg = 0
        article_neu = 0
        article_compo = 0
        for sent in sent_list:
            score = analyzer.polarity_scores(sent)
            article_pos += score['pos']
            article_neg += score['neg']
            article_neu += score['neu']
            article_compo += score['compound']
        length = len(sent_list)
        article_sentiment = pd.DataFrame([[article_pos / length, article_neg / length, article_neu / length,
                                           article_compo / length]],
                                         columns=('Positive', 'Negative', 'Neutral', 'Compound'))
        sentiment = sentiment.append(article_sentiment)
    sentiment.reset_index(drop=True, inplace=True)
    # print(df.describe())
    # print(sentiment.describe())
    # print(df.head())
    # print(sentiment.head())
    df = df.join(sentiment, how="inner")
    df.to_csv("sentiment.csv", index=False)
    sns.boxplot(y=df['Positive'], x=df['country_code'])
    plt.show()
    sns.boxplot(y=df['Negative'], x=df['country_code'])
    plt.show()
    sns.boxplot(y=df['Compound'], x=df['country_code'])
    plt.show()
    all_text = open("cloudText.txt", "r", encoding='utf-8').read()
    stop_words = set(STOPWORDS)
    stop_list = ["said", "will"]
    for word in stop_list:
        stop_words.add(word)
    word_cloud = WordCloud(background_color="white", height=860, width=1000, stopwords=stop_words).generate(all_text)
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    word_cloud.to_file("text.png")


def main():
    date = time.strftime('%Y-%m-%d', time.localtime())
    senti_score(date)


if __name__ == '__main__':
    main()
