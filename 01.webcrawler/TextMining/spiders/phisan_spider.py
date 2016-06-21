# -*- coding: utf-8 -*-
import scrapy
import csv
from TextMining.items import TextminingItem
from urlparse import urlparse
from urlparse import urljoin

class TextMiningSpider(scrapy.Spider):
    name = "phisan"
    cr = csv.reader(open("/Users/phisanshukkhi/Desktop/urllist.csv", "rb"))
    start_urls = [line[1].strip() for line in cr]

    # allowed_domains = [
    #     "thaiherb.most.go.th",
    # ]
    # start_urls = [
    #     'http://thaiherb.most.go.th/?q=herb',
    # ]

    def parse(self, response):
        selectors = [
            '//ul/li',
            '//ol/li',
            '//tr/td',
            '//div',
            '//p',
            '//font',
        ]
        for selector in selectors:
            for sel in response.xpath(selector):
                item = TextminingItem()
                titles = sel.xpath('a/text()').extract()
                links = sel.xpath('a/@href').extract()

                # for multiple links
                if len(links) != 0:
                    index = 0
                    for link in links:
                        item['link'] = link
                        r = urlparse(link)
                        item['netloc'] = r[1]

                        if len(titles) != 0:
                            item['title'] = titles[index]
                        else:
                            item['title'] = titles

                        # for relative path link
                        if item['netloc'] == '':
                            item['link'] = urljoin(response.url, link)
                            r = urlparse(item['link'])
                            item['netloc'] = r[1]

                        index += 1
                        yield item










