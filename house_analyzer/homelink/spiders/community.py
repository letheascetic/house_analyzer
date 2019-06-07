# -*- coding: utf-8 -*-

import random
import scrapy
import logging
import datetime

from utils import util
from conf import config
from urllib import parse
from mysql.sqlhl import SqlHl
from homelink.items import HlCommunityBasicInfoItem
from homelink.items import HlCommunityDynamicInfoItem
from twisted.internet.error import DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class CommunitySpider(scrapy.Spider):
    name = 'community'
    allowed_domains = ['sx.lianjia.com', 'nj.lianjia.com', 'hz.lianjia.com']

    logger = None
    sql_helper = None

    nj_districts = ['gulou', 'jianye', 'qinhuai', 'xuanwu', 'yuhuatai', 'qixia', 'jiangning', 'pukou', 'liuhe', 'lishui', 'gaochun']
    hz_districts = ['xihu', 'xiacheng', 'jianggan', 'gongshu', 'shangcheng', 'binjiang', 'yuhang', 'xiaoshan', 'tonglu1', 'chunan1', 'jiande',
                    'fuyang', 'linan', 'dajiangdong1', 'qiantangxinqu']

    community_ids = set()

    def __init__(self, *args, **kwargs):
        super(CommunitySpider, self).__init__(*args, **kwargs)
        self.sql_helper = SqlHl(config.MYSQL_CONFIG_PRODUCTION)
        self._init_logger()
        self._init_start_urls()

    def _init_logger(self):
        # util.config_logger()
        self.logger = logging.getLogger(__name__)

    def _init_start_urls(self):
        for district in self.nj_districts:
            self.start_urls.extend(['https://nj.lianjia.com/xiaoqu/{0}/pg{1}/'.format(district, page) for page in range(1, 31)])
        for district in self.hz_districts:
            self.start_urls.extend(['https://hz.lianjia.com/xiaoqu/{0}/pg{1}/'.format(district, page) for page in range(1, 31)])

        for city, community in self.sql_helper.get_all_communities():
            if city == 'nj' or city == 'hz':
                self.start_urls.append('https://{0}.lianjia.com/xiaoqu/rs{1}/'.format(city, community))

        random.shuffle(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, errback=self.err_back, priority=0)

    def parse(self, response):
        self.logger.info('parse url: {0}'.format(response.url))

        city = parse.urlparse(response.url).netloc.split('.')[0]
        record_date = datetime.datetime.now().strftime('%Y-%m-%d')

        community_selector_list = response.xpath('//ul[@class = "listContent"]/li')

        while len(community_selector_list) != 0:
            community_selector = community_selector_list.pop()
            community = community_selector.xpath('.//div[@class = "info"]/div[@class = "title"]/a/text()').extract_first().strip()
            community = community.replace('▪', '·')
            sold_recently = int(community_selector.xpath('.//div[@class = "houseInfo"]/a/text()').extract_first()[5:-1])
            on_sale = int(community_selector.xpath('.//div[@class = "xiaoquListItemSellCount"]/a/span/text()').extract_first())
            try:
                unit_price = float(community_selector.xpath('.//div[@class = "xiaoquListItemPrice"]/div[@class = "totalPrice"]/span/text()').extract_first())
            except:
                unit_price = None
                self.logger.info('parse community unit price exception[{0}].'.format(response.url))

            dynamic_item = HlCommunityDynamicInfoItem()
            dynamic_item['community'] = community
            dynamic_item['city'] = city
            dynamic_item['record_date'] = record_date
            dynamic_item['sold_recently'] = sold_recently
            dynamic_item['on_sale'] = on_sale
            dynamic_item['unit_price'] = unit_price
            yield dynamic_item

            href = community_selector.xpath('.//div[@class = "info"]/div[@class = "title"]/a/@href').extract_first()
            community_id = community_selector.xpath('./@data-id').extract_first()
            district = community_selector.xpath('.//div[@class = "positionInfo"]/a[@class = "district"]/text()').extract_first()
            location = community_selector.xpath('.//div[@class = "positionInfo"]/a[@class = "bizcircle"]/text()').extract_first()
            subway_info = community_selector.xpath('.//div[@class = "tagList"]/span/text()').extract_first()

            if community_id in self.community_ids:
                self.logger.info('community_id[{0}] already crawlered.'.format(community_id))
                return

            basic_item = HlCommunityBasicInfoItem()
            basic_item['community'] = community
            basic_item['city'] = city
            basic_item['community_id'] = community_id
            basic_item['district'] = district
            basic_item['location'] = location
            basic_item['subway_info'] = subway_info

            yield response.follow(href, meta={'item': basic_item}, callback=self.parse_basic_info, dont_filter=True)

    def parse_basic_info(self, response):
        self.logger.info('parse basic info url: {0}'.format(response.url))
        basic_item = response.meta['item']

        if basic_item['community_id'] not in response.url:
            self.logger.info('not right url for item[{0}]'.format(basic_item))
            return

        self.community_ids.add(basic_item['community_id'])

        address = response.xpath('//div[@class = "detailDesc"]/text()').extract_first()
        info = response.xpath('//div[@class = "xiaoquInfoItem"]/span[@class = "xiaoquInfoContent"]/text()').extract()

        basic_item['address'] = address
        basic_item['architectural_age'] = info[0]
        basic_item['architectural_type'] = info[1]
        basic_item['property_costs'] = info[2]
        basic_item['property_company'] = info[3]
        basic_item['developer'] = info[4]
        basic_item['total_buildings'] = info[5]
        basic_item['total_houses'] = info[6]

        yield basic_item

    def err_back(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        # in case you want to do something special for some errors,
        # you may need the failure's type:
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            self.logger.error('TimeoutError on %s', request.url)
