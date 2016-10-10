# -*- coding: utf-8 -*-
import json
import urllib
import urlparse
import re
import logging

import scrapy
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from twitter_spider.items import TweetItem
from twitter_spider.headers import Headers

logger = logging.getLogger('Tweet===Logger')

class TweetSpider(scrapy.Spider):
	name = '4tweets'
	base_tag_url = 'https://twitter.com/hashtag/%s?f=tweets&vertical=default&src=hash&lang=en-us'
	base_user_url = 'https://twitter.com/%s'
	base_tag_json_url = 'https://twitter.com/i/search/timeline?vertical=default&q=%s&src=hash&include_available_features=1&include_entities=1&lang=en-us&max_position=%s&reset_error_state=false'
	base_user_json_url = 'https://twitter.com/i/profiles/show/%s/timeline/tweets?include_available_features=1&include_entities=1&max_position=%s&reset_error_state=false'
	allowed_domains = ['twitter.com']

	custom_settings = {'FEED_URI' : 'file:///home/sasaki/dev/twitter/%(name)s/%(time)s.json', 
		'RETRY_TIMES' : 4}

	login_url = 'https://twitter.com/login'
	hashtags = ['ChicagoMarathon', 'FelizDomingo', 'Verstappen']
	
# Start from login and have cookie kept
	# def start_requests(self):
	# 	return [scrapy.Request(self.login_url, 
	# 		meta = {'cookiejar' : 1}, 
	# 		headers = Headers.login_headers,
	# 		callback = self.post_login)]

	# def post_login(self, response):
	# 	return [scrapy.FormRequest.from_response(response, 
	# 		meta = {'cookiejar' : response.meta['cookiejar']},
	# 		headers = Headers.login_headers, 
	# 		formdata = Headers.formdata, 
	# 		callback = self.after_login, 
	# 		dont_filter = True)]

	# def after_login(self, response):
	# 	for tag in hashtags:
	# 		next_tag_page = base_tag_url % urllib.quote_plus(tag)
	# 		yield scrapy.Request(next_tag_page, 
	# 			meta = {'cookiejar' : response.meta['cookiejar']},
	# 			callback = self.hashtag_parse,
	# 			headers = Headers.tag_headers % next_tag_page)

	def start_requests(self):
		for tag in self.hashtags:
				next_tag_page = self.base_tag_url % urllib.quote_plus(tag)
				yield scrapy.Request(next_tag_page, 
					callback = self.hashtag_parse)


# Applied to parse the entry urls, eg., hashtag pages.
	def hashtag_parse(self, response):
		first_page = response.body.replace('\n', '')
		for item in self.item_parse(first_page):
			yield item

		for tag in self.extract_tags(first_page, response.request.url):
			# Url passed to request receives UTF-8 params.
			next_tag_page = self.base_tag_url % urllib.quote_plus(tag.encode('utf-8'))
			yield scrapy.Request(next_tag_page, 
				callback = self.hashtag_parse)

# username allows only letter, number and _.
		for account in self.extract_accounts_inhash(first_page, response.request.url):
			next_user_page = self.base_user_url % urllib.quote_plus(account)
			yield scrapy.Request(next_user_page, 
				callback = self.user_parse)

		stream_foot = re.search(r'data-min-position="([^"]+?)"', first_page).group(1)
		tag_now = urlparse.urlparse(response.request.url).path.split('/')[-1].encode('utf-8')
		next_json_page = self.base_tag_json_url % (urllib.quote_plus(tag_now), urllib.quote_plus(stream_foot))
		if stream_foot:
			yield scrapy.Request(next_json_page, 
				callback = self.hashtag_stream_parse)


	def user_parse(self, response):
		first_page = response.body.replace('\n', '')
		for item in self.item_parse(first_page):
			yield item

		for tag in self.extract_tags(first_page, response.request.url):
			next_tag_page = self.base_tag_url % urllib.quote_plus(tag.encode('utf-8'))
			yield scrapy.Request(next_tag_page, 
				callback = self.hashtag_parse)

		for account in self.extract_accounts_inuser(first_page, response.request.url):
			next_user_page = self.base_user_url % urllib.quote_plus(account)
			yield scrapy.Request(next_user_page, 
				callback = self.user_parse)

		stream_foot = re.search(r'data-min-position="([^"]+?)"', first_page).group(1)
		user_now = urlparse.urlparse(response.request.url).path.split('/')[-1].encode('utf-8')
		next_json_page = self.base_user_json_url % (urllib.quote_plus(user_now), urllib.quote_plus(stream_foot))
		if stream_foot:
			yield scrapy.Request(next_json_page, 
				callback = self.user_stream_parse)


# Parse the stream json
	def hashtag_stream_parse(self, response):
		json_stream = json.loads(response.body)
		json_stream_html = json_stream['items_html'].encode('utf-8').replace('\n', '')

		for item in self.item_parse(json_stream_html):
			yield item

		for tag in self.extract_tags(json_stream_html, response.request.url):
			next_tag_page = self.base_tag_url % urllib.quote_plus(tag.encode('utf-8'))
			yield scrapy.Request(next_tag_page, 
				callback = self.hashtag_parse)

		for account in self.extract_accounts_inhash(json_stream_html, response.request.url):
			next_user_page = self.base_user_url % urllib.quote_plus(account)
			yield scrapy.Request(next_user_page, 
				callback = self.user_parse)

		if json_stream['has_more_items']:
			stream_foot = json_stream['min_position']
			tag_now = urlparse.parse_qs(urlparse.urlparse(response.request.url).query)['q'].encode('utf-8')
			next_json_page = self.base_tag_json_url % (urllib.quote_plus(tag_now), urllib.quote_plus(stream_foot))
			yield scrapy.Request(next_json_page, 
				callback = self.hashtag_stream_parse)


	def user_stream_parse(self, response):
		json_stream = json.loads(response.body)
		# json_stream['items_html'] is unicode.
		# After encoded into utf8, tags remain unicode.
		json_stream_html = json_stream['items_html'].encode('utf-8').replace('\n', '')

		for item in self.item_parse(json_stream_html):
			yield item

		for tag in self.extract_tags(json_stream_html, response.request.url):
			next_tag_page = self.base_tag_url % urllib.quote_plus(tag.encode('utf-8'))
			yield scrapy.Request(next_tag_page, 
				callback = self.hashtag_parse)

		for account in self.extract_accounts_inuser(json_stream_html, response.request.url):
			next_user_page = self.base_user_url % urllib.quote_plus(account)
			yield scrapy.Request(next_user_page, 
				callback = self.user_parse)

		if json_stream['has_more_items']:
			stream_foot = json_stream['min_position']
			user_now = urlparse.urlparse(response.request.url).path.split('/')[4].encode('utf-8')
			next_json_page = self.base_user_json_url % (urllib.quote_plus(user_now), urllib.quote_plus(stream_foot))
			yield scrapy.Request(next_json_page, 
				callback = self.user_stream_parse)


# Extract accounts or tags in different pages
	def extract_accounts_inhash(self, page_src, url):
		try:
			item_accounts = Selector(text = page_src).xpath('//span[@class="username js-action-profile-name"]/b/text()').extract()
			quoted_accounts = Selector(text = page_src).xpath('//span[@class="QuoteTweet-screenname u-dir"]/span/text()[2]').extract()
			mentioned_accounts = Selector(text = page_src).xpath('//a[@class="twitter-atreply pretty-link js-nav"]/b/text()').extract()
			return item_accounts + quoted_accounts + mentioned_accounts
		except Exception as e:
			logger.error('Meet some trouble in method [extract_accounts_inhash] ---- %s', url)

	def extract_accounts_inuser(self, page_src, url):
		try:
			quoted_accounts = Selector(text = page_src).xpath('//span[@class="QuoteTweet-screenname u-dir"]/span/text()[2]').extract()
			mentioned_accounts = Selector(text = page_src).xpath('//a[@class="twitter-atreply pretty-link js-nav"]/b/text()').extract()
			return quoted_accounts + mentioned_accounts
		except Exception as e:
			logger.error('Meet some trouble in method [extract_accounts_inuser] ---- %s', url)

	def extract_tags(self, page_src, url):
		try:
			# Page source keeps raw, so the coding tags look like u'\u4e2d\u56fd', already escaped.
			tags = Selector(text = page_src).xpath('//a[@class="twitter-hashtag pretty-link js-nav"]/b/text()').extract()
			return tags
		except Exception as e:
			logger.error('Meet some trouble in method [extract_tags] ---- %s', url)


# Load the fields into items
	def item_parse(self, page_src):
		for tweet_sel in Selector(text = page_src).xpath('//li[@class="js-stream-item stream-item stream-item"]/div'):
			try:
					item = TweetItem()
					item['user'] = tweet_sel.xpath('.//span[@class="username js-action-profile-name"]/b/text()').extract_first()
					item['content'] = "".join(tweet_sel.xpath('.//div[@class="js-tweet-text-container"]/p//text()').extract())
					# Quoted tweets displayed in two forms. One retweet without comments, one got.
					# item['quote_content'] = ("".join(tweet_sel.xpath('.//div[@class="QuoteTweet-text tweet-text u-dir"]//text()').extract()))
					item['timestamp'] = tweet_sel.xpath('.//a[@class="tweet-timestamp js-permalink js-nav js-tooltip"]/span[1]/@data-time-ms').extract_first()
					item['location'] = tweet_sel.xpath('.//span[@class="Tweet-geo u-floatRight js-tooltip"]/a/span[2]/text()').extract_first(default = '')
					item['retweets'] = tweet_sel.xpath('.//div[@class="ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt"]/button[1]/div[2]/span/span/text()').extract_first(default = '0')
					item['likes'] = tweet_sel.xpath('.//div[@class="ProfileTweet-action ProfileTweet-action--favorite js-toggleState"]//span[@class="ProfileTweet-actionCountForPresentation"]/text()').extract_first(default = '0')
					yield item
			except Exception as e:
				logger.error('Meet some trouble in method [item_parse] while parsing ---- %s', tweet_sel.xpath('.').extract_first())
