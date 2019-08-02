import pandas as pd
import re
from nltk.tokenize import sent_tokenize


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""

    if '\u4e00' <= uchar <= '\u9fff':

        return True

    else:

        return False


def generate_ennews():
    """
    将所有的英文新闻存入enNews.csv中
    """
    df = pd.read_csv('07-12.csv')
    pat = re.compile('<[^>]*>')
    for i in range(len(df.iloc[:, 5]))[::-1]:
        sentence_list = sent_tokenize(pat.sub('', df.iloc[:, 8][i]).strip().replace('\n', ''))
        if len(sentence_list) == 0:
            df = df.drop([i])
            continue
        title = df.iloc[:, 5][i]
        for char in title:
            if is_chinese(char):
                df = df.drop([i])
                break

    df.to_csv("07-12enNews.csv", encoding='utf-8', index=False)






if __name__ == "__main__":
    generate_ennews()

