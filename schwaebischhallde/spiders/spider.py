import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import SchwaebischhalldeItem
from itemloaders.processors import TakeFirst


class SchwaebischhalldeSpider(scrapy.Spider):
	name = 'schwaebischhallde'
	start_urls = ['https://newsroom.schwaebisch-hall.de/presseinformationen/']

	def parse(self, response):
		post_links = response.xpath('//div[@aria-live="polite"]//div[@class="tile__content__footer"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="article__title"]/text()').get()
		description = response.xpath('//div[@class="article__content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="article__meta"]/text()').get()
		if date:
			date = re.findall(r'\d{2}\.\d{2}\.\d{4}', date)[0]

		item = ItemLoader(item=SchwaebischhalldeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
