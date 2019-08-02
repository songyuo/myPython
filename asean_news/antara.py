import re
import time
from util import NewsCrawler


class AntaraCrawler(NewsCrawler):
    """  爬取https://en.antaranews.com，印度尼西亚  """

    category = {
        'national': [],
        'international': [],
        'business': [],
        'election': []
    }

    base_url = 'https://en.antaranews.com'

    query = 'div.col-md-8  h3 > a'

    date_format = [
        r'<span class="article-date"><i class="fa fa-clock-o"></i> (.*)</span>',
        r'<div class="entry-header">.*?<i class="fa fa-clock-o"></i>[\s]*(.*?)[ ]?[\d]*[:]?[\d]*[\s]*</li>'
    ]

    country = 'Indonesia'

    page_format = '/'

    # only_today = False

    # test = True

    show_error = False

    max_page = 5

    def get_date(self, article):
        if 'pemilu' not in article.url:
            pattern = re.compile(self.date_format[0])
        else:
            pattern = re.compile(self.date_format[1], re.DOTALL)
        try:
            date = pattern.findall(article.html)[0].replace('st', '').replace('nd', '').replace('th', '').replace(
                                  'rd', '').replace('Augu', 'August')
        except IndexError:
            return None
        if 'ago' in date:
            return time.strftime('%Y-%m-%d', time.localtime())
        else:
            try:
                date = time.strptime(date, '%d %B %Y')
                date = time.strftime('%Y-%m-%d', date)
            except ValueError:
                return None
            else:
                return date

    def start_url(self):
        for class_1 in self.category.keys():
            self.items.extend([class_1, None])
            if class_1 == 'election':
                self.base_url = 'https://pemilu.antaranews.com'
                url = self.base_url + '/english'
            elif class_1 == 'business':
                url = self.base_url + '/' + 'bussiness'
            else:
                url = self.base_url + '/' + class_1
            for i in range(1, self.page + 1):
                if self.stop_yield:
                    self.stop_yield = False
                    break
                yield url + self.page_format + str(i)
            self.items[2:] = []


if __name__ == '__main__':
    AntaraCrawler.run()

