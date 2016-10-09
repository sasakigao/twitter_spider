# twitter_spider
Take hashtags as entries and scrape the tweets, including stream contents, by python Scrapy.

# Spider entry
Defined by hashtags, then scrape tweets from users pages and tags pages.

# About encoding
Twitter returns a `utf-8` page for the first page of a stream, and `unicode` pages for the ajax calls
later on.
I do nothing on the first page, but load the second one into json objects and extract the `items_html`
, as well as the html body, encode it into `utf-8` and remove `\n`, make the stream parsable.