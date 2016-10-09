# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TweetItem(scrapy.Item):
	user = scrapy.Field()
	content = scrapy.Field()
	quote_content = scrapy.Field()
	timestamp = scrapy.Field()
	location = scrapy.Field()
	retweets = scrapy.Field()
	likes = scrapy.Field()
	source = scrapy.Field()
