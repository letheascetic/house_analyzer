# -*- coding: utf-8 -*-

import random
import scrapy
import logging

from homelink.utils import util
from homelink.conf import config
from homelink.items import HomelinkItem
from homelink.db.homelink import SqlHomeLink
from twisted.internet.error import DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class SxSpider(scrapy.Spider):
    name = 'sx'
    allowed_domains = ['sx.lianjia.com']

    house_ids = set()
    logger = None
    sql_helper = None

    def __init__(self, *args, **kwargs):
        super(SxSpider, self).__init__(*args, **kwargs)
        self.sql_helper = SqlHomeLink(config.DB_CONFIG)
        self._init_logger()
        self._init_start_urls()

    def _init_logger(self):
        util.config_logger()
        self.logger = logging.getLogger(__name__)

    def _init_start_urls(self):
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/keqiaoqu/pg{0}/'.format(page) for page in range(1, 101)])
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/yuechengqu/pg{0}/'.format(page) for page in range(1, 101)])
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/shangyuqu/pg{0}/'.format(page) for page in range(1, 11)])
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/shengzhoushi/pg{0}/'.format(page) for page in range(1, 11)])
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/xinchangxian/pg{0}/'.format(page) for page in range(1, 11)])
        self.start_urls.extend(
            ['https://sx.lianjia.com/ershoufang/zhujishi/pg{0}/'.format(page) for page in range(1, 11)])
        random.shuffle(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True,
                                 errback=self.err_back, priority=0)

    def parse(self, response):
        self.logger.info('current url: {0}'.format(response.url))

        hrefs = set(response.xpath('//a[re:match(@href, "ershoufang/.+html")]/@href').extract())
        for href in hrefs:
            yield response.follow(href, callback=self.parse_details, dont_filter=True)

    def parse_details(self, response):
        self.logger.info('current detail url: {0}'.format(response.url))

        if response.url.find('sx.lianjia.com') < 0:
            self.logger.info('not shao xing house info: [{0}]'.format(response.url))
            return

        house_id = response.url.split('/')[-1].split('.')[0]
        if house_id in self.house_ids:
            self.logger.info('house id already crawled: [{0}]'.format(response.url))
            return

        self.house_ids.add(house_id)
        item = HomelinkItem()

        item['city'] = 'sx'
        item['house_id'] = house_id

        item['total_price'] = float(response.xpath('//div/span[@class = "total"]/text()').extract_first())
        item['unit_price'] = float(response.xpath('//span[@class = "unitPriceValue"]/text()').extract_first())

        item['room_info'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "room"]/div[@class = "mainInfo"]/text()').extract_first()
        item['floor_info'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "room"]/div[@class = "subInfo"]/text()').extract_first()

        item['orientation'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "type"]/div[@class = "mainInfo"]/text()').extract_first()
        item['decoration'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "type"]/div[@class = "subInfo"]/text()').extract_first()

        item['house_size'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "area"]/div[@class = "mainInfo"]/text()').extract_first()
        item['house_type'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "area"]/div[@class = "subInfo"]/text()').extract_first()

        item['community'] = response.xpath('//div[@class = "aroundInfo"]/div[@class = "communityName"]//a[contains(@class, "info")]/text()').extract_first()
        item['district'] = response.xpath('//div[@class = "aroundInfo"]/div[@class = "areaName"]//a/text()').extract()[0]
        item['location'] = response.xpath('//div[@class = "aroundInfo"]/div[@class = "areaName"]//a/text()').extract()[-1]

        basic_info = response.xpath('//div[@class = "introContent"]/div[@class = "base"]/div[@class = "content"]/ul/li/text()').extract()
        if len(basic_info) >= 14:
            item['room_structure'] = basic_info[3]
            # item['room_size'] = basic_info[4]
            item['room_size'] = round(item['total_price']/item['unit_price'], 2)
            item['building_structure'] = basic_info[7]
            item['elevator_household_ratio'] = basic_info[9]
            item['elevator_included'] = basic_info[10]
            item['property_right_deadline'] = basic_info[11]
        elif len(basic_info) == 9:
            item['room_structure'] = None
            # item['room_size'] = basic_info[3]
            item['room_size'] = round(item['total_price'] / item['unit_price'], 2)
            item['building_structure'] = basic_info[5]
            item['elevator_household_ratio'] = None
            item['elevator_included'] = None
            item['property_right_deadline'] = basic_info[8]
        elif len(basic_info) == 12:
            item['room_structure'] = basic_info[3]
            # item['room_size'] = basic_info[4]
            item['room_size'] = round(item['total_price'] / item['unit_price'], 2)
            item['building_structure'] = basic_info[7]
            item['elevator_household_ratio'] = basic_info[9]
            item['elevator_included'] = basic_info[10]
            item['property_right_deadline'] = basic_info[11]
        else:
            self.logger.warning('not xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx shao xing house info: [{0}]'.format(response.url))
            return

        transaction_info = response.xpath('//div[@class = "introContent"]/div[@class = "transaction"]/div[@class = "content"]/ul/li/span[not(@class)]/text()').extract()
        item['list_date'] = transaction_info[0]
        item['last_trading_date'] = transaction_info[2]

        yield item

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
