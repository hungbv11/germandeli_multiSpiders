# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from datetime import date


class SeasonalSpider(scrapy.Spider):
    name = "seasonal2"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://www.germandeli.com/Seasonal/Christmas',
                  'http://www.germandeli.com/Seasonal/Easter_Specialties',
                  'http://www.germandeli.com/Seasonal/Greeting_Cards',
                  'http://www.germandeli.com/Seasonal/Oktoberfest',
                  'http://www.germandeli.com/Seasonal/Silvester_New_Years_Eve',
                  'http://www.germandeli.com/Seasonal/Valentines_Day',]
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/seasonal'}

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href').extract()
        for url in urls:
            if url is not None:
                yield scrapy.Request("http://www.germandeli.com/"+str(url), self.parse_page)
                print(url)

    def parse(self, response):
        urls = response.xpath('*//div[@class="category-cell-name"]/a/@href')
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com/"+str(url.extract()), self.parse_page)
            print(url)

    def parse_page(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href')
        for url in urls:
            yield SplashRequest("http://www.germandeli.com" + str(url.extract()), self.parse_product,
                                args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,
                                    'timeout': 10,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.html',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )
            #print(url)

        next = response.xpath('*//div[@class="pagination pagination-small pull-right"]/ul/li[3]/a/@href')
        yield SplashRequest("http://www.germandeli.com" + str(next.extract_first()), self.parse_page,
                            args={
                                    # optional; parameters passed to Splash HTTP API
                                    'wait': 0.5,
                                    'timeout': 10,

                                    # 'url' is prefilled from request url
                                    # 'http_method' is set to 'POST' for POST requests
                                    # 'body' is set to request body for POST requests
                                },
                                endpoint='render.html',  # optional; default is render.html
                                # splash_url='<url>',  # optional; overrides SPLASH_URL
                                # slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
                                )


    def parse_product(self, response):
        name_ = str(response.xpath('//*[@itemprop="name"]/text()').extract_first())
        name_ = name_.replace("\t", "")
        name_ = name_.replace("\n", "")
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()
        #image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()
        update_on_ = date.today().isoformat()
        price_ = response.xpath('//*[@itemprop="price"]/text()').extract()
        if(1 <= len(price_)):
            price_temp = str(price_[1])
            price_temp = price_temp.replace("\t", "")
            price_temp = price_temp.replace("\n", "")
            if(1 <= len(ingredients_)):
                ingredients_temp = str(ingredients_[1])
                ingredients_temp = ingredients_temp.replace("\t", "")
                ingredients_temp = ingredients_temp.replace("\n", "")
                ingredients_temp = ingredients_temp.replace("  ", "")
                yield GermandeliItem(name=name_, price=price_temp, ingredients=ingredients_temp, description=description_,
                                     update_on=update_on_, file_urls=[image_url_])
