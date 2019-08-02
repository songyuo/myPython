from util import NewsCrawler


class JakartaCrawler(NewsCrawler):

    country = 'Indonesia'

    base_url = 'https://www.thejakartapost.com'

    category = {
        ''
    }

    max_page = 4000