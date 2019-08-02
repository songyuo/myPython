# -*- coding: utf-8 -*-
import scrapy


class ThestarSpider(scrapy.Spider):
    name = 'thestar'
    allowed_domains = ['www.thestar.com.my']
    start_urls = ['http://www.thestar.com.my/']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
