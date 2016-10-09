
class Headers(object):
	"""docstring for ClassName"""
	
	login_headers = {"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"accept-encoding" : "gzip, deflate, sdch, br",
		"accept-language" : "en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
		"connection" : "keep-alive",
		"content-type" : " application/x-www-form-urlencoded; charset=UTF-8",
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
		"upgrade-insecure-requests" : "1",
		"referer" : "https://twitter.com/login"}

	tag_headers = {"accept" : "application/json, text/javascript, */*; q=0.01",
		"accept-encoding" : "gzip, deflate, sdch, br",
		"accept-language" : "en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
		"referer" : "%s",
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
		"x-asset-version" : "a8caba",
		"x-push-state-request" : "true",
		"x-requested-with" : "XMLHttpRequest"}

	user_headers = {"accept" : "application/json, text/javascript, */*; q=0.01",
		"accept-encoding" : "gzip, deflate, sdch, br",
		"accept-language" : "en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
		"referer" : "%s",
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
		"x-asset-version" : "a8caba",
		"x-push-state-request" : "true",
		"x-requested-with" : "XMLHttpRequest"}

	tag_stream_headers = {"accept" : "application/json, text/javascript, */*; q=0.01",
		"accept-encoding" : "gzip, deflate, sdch, br",
		"accept-language" : "en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
		"referer" : "%s",
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
		"x-requested-with" : "XMLHttpRequest"}

	user_stream_headers = {"accept" : "application/json, text/javascript, */*; q=0.01",
		"accept-encoding" : "gzip, deflate, sdch, br",
		"accept-language" : "en,en-US;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2",
		"referer" : "%s",
		"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36",
		"x-requested-with" : "XMLHttpRequest"}

	formdata = {'session[username_or_email]' : 'sasakigao@gmail.com',
		'session[password]' : '19920807',
		'authenticity_token' : '2e3f3e03dad92ffd6082fcc96f6629a02ee9e2e6',
		'return_to_ssl' : 'true',
		'authenticity_token' : '2e3f3e03dad92ffd6082fcc96f6629a02ee9e2e6',
		'remember_me' : '1'}		