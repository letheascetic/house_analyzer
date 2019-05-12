# -*- coding: utf-8 -*-

BOT_NAME = 'house_analyzer'

SPIDER_MODULES = ['homelink.spiders']
NEWSPIDER_MODULE = 'homelink.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 4
COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

ITEM_PIPELINES = {
    'homelink.pipelines.FilterPipeline': 300,
}
