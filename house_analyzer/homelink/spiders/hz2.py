# -*- coding: utf-8 -*-

import random
import scrapy
import logging
import datetime

from utils import util
from conf import config
from mysql.sqlhl import SqlHl
from homelink.items import HomelinkItem
from twisted.internet.error import DNSLookupError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class Hz2Spider(scrapy.Spider):
    name = 'hz2'
    allowed_domains = ['hz.lianjia.com']

    house_ids = set()
    logger = None
    sql_helper = None

    def __init__(self, *args, **kwargs):
        super(Hz2Spider, self).__init__(*args, **kwargs)
        self.sql_helper = SqlHl(config.MYSQL_CONFIG_PRODUCTION)
        self._init_logger()
        self._init_start_urls()

    def _init_logger(self):
        # util.config_logger()
        self.logger = logging.getLogger(__name__)

    def _init_start_urls(self):
        for city, community in self.sql_helper.get_all_communities():
            if city == 'hz':
                self.start_urls.extend(['https://hz.lianjia.com/ershoufang/pg{0}rs{1}/'.format(page, community) for page in range(1, 11)])
                self.start_urls.extend(['https://hz.lianjia.com/chengjiao/pg{0}rs{1}/'.format(page, community) for page in range(1, 11)])
        random.shuffle(self.start_urls)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, errback=self.err_back, priority=0)

    def parse(self, response):
        self.logger.info('current url: {0}'.format(response.url))

        hrefs = set(response.xpath('//a[re:match(@href, "ershoufang/.+html")]/@href').extract())
        hrefs = hrefs.union(set(response.xpath('//a[re:match(@href, "chengjiao/.+html")]/@href').extract()))
        for href in hrefs:
            house_id = href.split('/')[-1].split('.')[0]
            if house_id in self.house_ids:
                self.logger.info('house id already crawled: [{0}]'.format(response.url))
            else:
                self.house_ids.add(house_id)
                yield response.follow(href, callback=self.parse_details, dont_filter=True)

    def parse_details(self, response):
        self.logger.info('current detail url: {0}'.format(response.url))

        if response.url.find('hz.lianjia.com') < 0:
            self.logger.info('not hang zhou house info: [{0}]'.format(response.url))
            return

        house_id = response.url.split('/')[-1].split('.')[0]

        self.house_ids.add(house_id)

        if 'ershoufang' in response.url:
            item = self.get_selling_house_detail(response)
        elif 'chengjiao' in response.url:
            item = self.get_sold_house_detail(response)
        else:
            self.logger.info('not matching url:[{0}]'.format(response.url))
            item = None

        if item is not None:
            yield item

    def get_sold_house_detail(self, response):
        house_id = response.url.split('/')[-1].split('.')[0]

        # 必填项
        item = HomelinkItem()
        item['url'] = response.url
        item['city'] = 'hz'
        item['house_id'] = house_id

        status_tag = response.xpath('//div/div[@class = "wrapper"]/span/text()').extract_first()
        if status_tag is None:
            return

        self.logger.info('house[{0}] status:[{1}]'.format(house_id, status_tag))
        if '成交' in status_tag:
            item['status'] = config.HOUSE_STATUS['DEAL']        # status=4,表示已成交
        else:
            item['status'] = config.HOUSE_STATUS['DEAL_OTHER']  # status=5,其他情况

        # 成交房源必填的数据项
        item['deal_date'] = '-'.join(status_tag.split(' ')[0].split('.'))
        item['deal_total_price'] = float(response.xpath('//div/span[@class = "dealTotalPrice"]/i/text()').extract_first())
        item['deal_unit_price'] = float(response.xpath('//div[@class = "price"]/b/text()').extract_first())

        item['list_total_price'] = float(response.xpath('//div[@class = "msg"]/span/label/text()').extract_first())
        try:
            item['deal_time_span'] = int(response.xpath('//div[@class = "msg"]/span/label/text()').extract()[1])
        except Exception as e:
            self.logger.warning('convert deal time span exception: [{0}]'.format(e))
            item['deal_time_span'] = None
        item['price_change_times'] = int(response.xpath('//div[@class = "msg"]/span/label/text()').extract()[2])

        # 成交房源可获取到的其他数据项
        info = response.xpath('//div/div[@class = "wrapper"]/text()').extract_first().split(' ')
        community = ''.join(info[0:-2])
        item['community'] = community.replace('▪', '·')
        item['room_info'] = info[-2]

        item['district'] = response.xpath('//div[@class = "myAgent"]/div[@class = "name"]/a/text()').extract()[0]
        item['location'] = response.xpath('//div[@class = "myAgent"]/div[@class = "name"]/a/text()').extract()[-1]

        item['total_price'] = item['deal_total_price']
        item['unit_price'] = item['deal_unit_price']
        item['house_size'] = round(item['total_price'] / item['unit_price'] * 10000, 2)

        if item['deal_time_span'] is not None:
            list_date = datetime.datetime.strptime(item['deal_date'], "%Y-%m-%d") - datetime.timedelta(days=item['deal_time_span'])
            item['list_date'] = list_date.strftime('%Y-%m-%d')
        else:
            item['list_date'] = None

        item['list_unit_price'] = round(item['list_total_price'] / item['house_size'] * 10000, 2)

        return item

    def get_selling_house_detail(self, response):
        house_id = response.url.split('/')[-1].split('.')[0]

        # 必填项
        item = HomelinkItem()
        item['url'] = response.url
        item['city'] = 'hz'
        item['house_id'] = house_id

        status_tag = response.xpath('//h1[@class = "main"]/span/text()').extract_first()
        self.logger.info('house[{0}] status:[{1}]'.format(house_id, status_tag))
        if status_tag is None:
            item['status'] = config.HOUSE_STATUS['ON_SALE']  # status=1,表示正常
        elif status_tag == '已下架':
            item['status'] = config.HOUSE_STATUS['OFF_SALE']  # status=2,表示已下架
        else:
            item['status'] = config.HOUSE_STATUS['ON_SALE_OTHER']  # status=3,表示其他状态

        # item['deal_date'] = None

        item['total_price'] = float(response.xpath('//div/span[@class = "total"]/text()').extract_first())
        item['unit_price'] = float(response.xpath('//span[@class = "unitPriceValue"]/text()').extract_first())

        item['room_info'] = response.xpath(
            '//div[@class = "houseInfo"]/div[@class = "room"]/div[@class = "mainInfo"]/text()').extract_first()
        item['floor_info'] = response.xpath(
            '//div[@class = "houseInfo"]/div[@class = "room"]/div[@class = "subInfo"]/text()').extract_first()

        item['orientation'] = response.xpath(
            '//div[@class = "houseInfo"]/div[@class = "type"]/div[@class = "mainInfo"]/text()').extract_first()
        item['decoration'] = response.xpath(
            '//div[@class = "houseInfo"]/div[@class = "type"]/div[@class = "subInfo"]/text()').extract_first()

        # item['house_size'] = response.xpath('//div[@class = "houseInfo"]/div[@class = "area"]/div[@class = "mainInfo"]/text()').extract_first()
        item['house_size'] = round(item['total_price'] / item['unit_price'] * 10000, 2)
        item['house_type'] = response.xpath(
            '//div[@class = "houseInfo"]/div[@class = "area"]/div[@class = "subInfo"]/text()').extract_first()

        community = ''.join(response.xpath(
            '//div[@class = "aroundInfo"]/div[@class = "communityName"]//a[contains(@class, "info")]/text()').extract_first().split(' '))
        item['community'] = community.replace('▪', '·')

        location_info = response.xpath('//div[@class = "aroundInfo"]/div[@class = "areaName"]//a/text()').extract()
        if len(location_info) == 3:
            item['district'], item['location'], item['subway_info'] = location_info
        elif len(location_info) == 2:
            item['district'] = location_info[0]
            item['location'] = location_info[1]
            item['subway_info'] = None
        else:
            item['district'] = location_info[0]
            item['location'] = None
            item['subway_info'] = None

        # get basic info
        basic_info = response.xpath(
            '//div[@class = "introContent"]/div[@class = "base"]/div[@class = "content"]/ul/li/text()').extract()
        if len(basic_info) >= 14:
            item['room_structure'] = basic_info[3]
            item['room_size'] = basic_info[4]
            item['building_structure'] = basic_info[7]
            item['elevator_household_ratio'] = basic_info[9]
            item['elevator_included'] = basic_info[10]
            item['property_right_deadline'] = basic_info[11]
        elif len(basic_info) == 9:
            item['room_structure'] = None
            item['room_size'] = basic_info[3]
            item['building_structure'] = basic_info[5]
            item['elevator_household_ratio'] = None
            item['elevator_included'] = None
            item['property_right_deadline'] = basic_info[8]
        elif len(basic_info) == 12:
            item['room_structure'] = basic_info[3]
            item['room_size'] = basic_info[4]
            item['building_structure'] = basic_info[7]
            item['elevator_household_ratio'] = basic_info[9]
            item['elevator_included'] = basic_info[10]
            item['property_right_deadline'] = basic_info[11]
        else:
            self.logger.warning('not xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx hang zhou house info: [{0}]'.format(response.url))
            return

        # get transaction info
        transaction_info = response.xpath('//div[@class = "introContent"]/div[@class = "transaction"]/div[@class = "content"]/ul/li/span[not(@class)]/text()').extract()
        item['list_date'] = transaction_info[0]
        item['last_trading_date'] = transaction_info[2]

        return item

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
