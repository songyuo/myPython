from util import NewsCrawler


class PhnoCrawler(NewsCrawler):
    """  爬取www.phnompenhpost.com，柬埔寨  """

    category = {
        'national': ['post-depth', 'politics-0', 'kr-tribunal'],
        'business': ['post-property', 'post-focus', 'post-auto', 'special-reports'],
        'opinion': ['opinion'],
        'international': ['international']
    }

    base_url = 'https://www.phnompenhpost.com'

    query = 'div.item-list ul li h3 a'

    country = 'Cambodia'

    date_format = [[r'Publication date (.*) \|', r', (.*, .{4}) \| by '], ['%d %B %Y', '%B %d, %Y']]

    max_page = 1

    # only_today = True

    # test = True

    show_error = False


if __name__ == '__main__':
    PhnoCrawler.run()




