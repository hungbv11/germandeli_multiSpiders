# -*- coding: utf-8 -*-
import scrapy
from germandeli_multiSpiders.items import GermandeliMultispidersItem
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from datetime import date


class NonfoodSpider(scrapy.Spider):
    name = "nonfood1"
    allowed_domains = ["germandeli.com"]
    start_urls = ['http://www.germandeli.com/NonFood/Black-Red-and-Gold',
                  'http://www.germandeli.com/NonFood/Cutlery_and_Accessories',
                  'http://www.germandeli.com/NonFood/Feuerzangenbowle',
                  'http://www.germandeli.com/NonFood/German_Pottery__Porcelain',
                  'http://www.germandeli.com/NonFood/PorcelainGlass',
                  'http://www.germandeli.com/NonFood/Raclette_and_Fondue',
                  'http://www.germandeli.com/NonFood/Raetsel_2',
                  'http://www.germandeli.com/NonFood/Rumtopf_Rum_Pot_Pottery',
                  'http://www.germandeli.com/NonFood/Spaetzle_Presses',
                  'http://www.germandeli.com/NonFood/Indoor-Plant-Supplies',
                  'http://www.germandeli.com/NonFood/PorcelainGlass',
                  'http://www.germandeli.com/NonFood/Buecher_Romane_Raetsel_uzw/Kinder-Buecher',
                  'http://www.germandeli.com/NonFood/Housewares/Barware/Swissmar_Barware',
                  ]
    custom_settings = {'FILES_STORE': '/home/hung/Projects/germandeli_multiSpiders/output/nonfood1'}

    def parse(self, response):
        urls = response.xpath('*//h2[@class="item-cell-name"]/a/@href').extract()
        print(urls)
        for url in urls:
            yield scrapy.Request("http://www.germandeli.com" + str(url), self.parse_product)
            print(url)

    def parse_product(self, response):
        name_ = str(response.xpath('//*[@itemprop="name"]/text()').extract_first())
        ingredients_ = response.xpath('//*[@id="ingredients"]/text()').extract()
        description_ = response.xpath('*//div[@class="tab-pane active in"]/ul/li/text()').extract()
        image_ = response.xpath('//*[@itemprop="image"]/@src')
        image_url_ = response.xpath('//*[@itemprop="image"]/@src').extract_first()
        update_on_ = date.today().isoformat()
        price_ = str(response.xpath('//*[@itemprop="price"]/text()').extract()[0])
        # else:
        #     price_temp = str(price_[1])
        # if(1 <= len(ingredients_)):
        #    ingredients_temp = ingredients_[1]
        yield GermandeliMultispidersItem(name= name_, price= price_, ingredients = ingredients_, description=description_,
                                         update_on= update_on_, file_urls= [image_url_])