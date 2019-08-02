# -*- coding: utf-8 -*-
import scrapy

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/get']
    '烦的呀儿匹'

    def parse(self, response):
        self.logger.debug(response.text)
        self.logger.debug('status code:' + str(response.status))
