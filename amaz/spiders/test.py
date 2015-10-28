# -*- coding: utf-8 -*-
import scrapy
from amaz.items import AmazItem
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
import re

class TestSpider(scrapy.Spider):
	name = "test"
	download_delay = 1
	allowed_domains = ["amazon.cn"]
	start_urls = (
		'http://www.amazon.cn/gp/product/B00OZIDK6E/',
	)

	def parse(self, response):
		sel = Selector(response)
		'''
		for asin in asins:
			item = AmazItem()
			item['asin'] = asin
			yield item
		'''

		item = AmazItem()
		item['asin'] = response.xpath('//input[@name="ASIN.0"]/@value').extract_first().strip()
		item['title'] =	response.xpath('//span[@id="btAsinTitle"]/span/text()').extract_first().strip()
		item['price'] = response.xpath('//b[@class="priceLarge"]/text()').extract_first().strip()
		'''
		item = AmazItem()
		item['asin'] = response.xpath('//input[@name="ASIN.0"]/@value').re('\S+')
		item['title'] =	response.xpath('//span[@id="btAsinTitle"]/span/text()').re('\S+')
		item['price'] = response.xpath('//b[@class="priceLarge"]/text()').re('\S+')
		'''
		yield item


		asins = sel.xpath('//body').re('B0\w\w\w\w\w\w\w\w')



		for asin in asins:
    			asin = "http://www.amazon.cn/gp/product/" + asin
    			yield Request(asin, callback=self.parse)


