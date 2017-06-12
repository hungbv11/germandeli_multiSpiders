# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest


class SeasonalSpider(scrapy.Spider):
    name = "seasonal"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://germandeli.com']

    def parse(self, response):
        category_links = response.xpath('*//ul[@class="nav"]/li/a/@href').extract()
        for link in category_links:
            yield scrapy.Request("http://germandeli.com"+link, self.parse_page)

    def parse_page(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http://germandeli.com/"+url, self.parse_page_sub)

    def parse_page_sub(self, response):  # using spash for scraping each sub-category
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        for url in urls:
            yield SplashRequest("http://germandeli.com" + url, self.parse_product,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,
                                    # 'timeout': 10,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.html',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )
            print(url)

        # also need to add splash in this
        next = response.xpath(
            '*//ul[@class="pagination-links"]/li[3]/a/@href').extract()  # need to test the li[3] with scrapy shell again
        yield SplashRequest("http://germandeli.com" + next, self.parse_page_sub,
                            args={
                                # optional; parameters passed to Splash HTTP API
                                'wait': 0.5,
                                # 'timeout': 10,

                                # 'url' is prefilled from request url
                                # 'http_method' is set to 'POST' for POST requests
                                # 'body' is set to request body for POST requests
                            },
                            endpoint='render.html',  # optional; default is render.html
                            # splash_url='<url>',  # optional; overrides SPLASH_URL
                            # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                            )
        print(next)

    def parse_product(self, response):#need to use the spash for scraping the ingredients
        #grab the url of the product image
        image = response.css("").xpath("@src")
        image_url = image.extract_first()

        #grab the name, price, description and ingredients
        name = response.xpath('//*[@itemprop="name"]/text()').extract_first()
        price = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        description = list()
        description[0] = response.xpath('*//div[@class="tab-pane active in"]/ul/li[1]/text()').extract()
        description[1] = response.xpath('*//div[@class="tab-pane active in"]/ul/li[2]/text()').extract()
        description[2] = response.xpath('*//div[@class="tab-pane active in"]/ul/li[3]/text()').extract()
        description[3] = response.xpath('*//div[@class="tab-pane active in"]/ul/li[4]/text()').extract()
        description[4] = response.xpath('*//div[@class="tab-pane active in"]/ul/li[5]/text()').extract()
        ingredients = response.xpath('//*[@id="ingredients"]/text()').extract()

        #yield the result and check about the splash for ingredients
        yield SeasonalSpider(name = name, price = price, description = description, ingredients = ingredients, image_url =[image_url])



