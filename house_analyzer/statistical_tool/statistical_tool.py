# coding: utf-8


import logging
import datetime

from utils import util
from conf import config
from mysql.sqlhl import SqlHl
from mysql.base import HlCommunityDynamicInfo


class StatisticalTool:

    def __init__(self):
        self._init_logger()
        self.sql_helper = SqlHl(config.MYSQL_CONFIG_TESTING)
        pass

    def _init_logger(self):
        util.config_logger()
        self.logger = logging.getLogger(__name__)

    def do_statistics(self):

        today = datetime.datetime.utcnow()

        for city, community in self.sql_helper.get_all_communities():
            self.logger.info('start to statistics city[{0}], community[{1}]'.format(city, community))
            statistical_date = self.sql_helper.get_community_last_statistical_date(city, community)
            if statistical_date is not None and statistical_date.year == today.year and statistical_date.month == today.month:
                self.logger.info('community[{0}] already has statistics.'.format(community))
                continue

            community_info = HlCommunityDynamicInfo(city=city, community=community, statistical_date=today.strftime('%Y-%m-%d'))
            community_info.total_on_sale, community_info.total_off_sale, community_info.total_sold = 0, 0, 0
            for status, num in self.sql_helper.get_community_total_status(city, community):
                self.logger.info('community[{0}] total status[{1}:{2}].'.format(community, status, num))
                if status == config.HOUSE_STATUS['ON_SALE']:
                    community_info.total_on_sale = num
                elif status == config.HOUSE_STATUS['OFF_SALE']:
                    community_info.total_off_sale = num
                elif status == config.HOUSE_STATUS['DEAL']:
                    community_info.total_sold = num
                else:
                    pass

            if today.month != 1:
                time_begin = datetime.datetime(today.year, today.month-1, 1).strftime('%Y-%m-%d')
            else:
                time_begin = datetime.datetime(today.year - 1, 12, 1).strftime('%Y-%m-%d')
            time_end = datetime.datetime(today.year, today.month, 1).strftime('%Y-%m-%d')

            new_on_sale = self.sql_helper.get_community_new_on_sale(city, community, time_begin, time_end)
            self.logger.info('community[{0}] new on sale[{1}].'.format(community, new_on_sale))
            community_info.new_on_sale = new_on_sale

            new_off_sale = self.sql_helper.get_community_new_off_sale(city, community, time_begin, time_end)
            self.logger.info('community[{0}] new off sale[{1}].'.format(community, new_off_sale))
            community_info.new_off_sale = new_off_sale

            new_sold = self.sql_helper.get_community_new_sold(city, community, time_begin, time_end)
            self.logger.info('community[{0}] new sold[{1}].'.format(community, new_sold))
            community_info.new_sold = new_sold

            total_on_sale_info = {}
            for house_id, house_size, record_date, total_price, unit_price in self.sql_helper.get_community_total_on_sale_unit_price(city, community):
                if house_id not in total_on_sale_info.keys() or (house_id in total_on_sale_info.keys() and total_on_sale_info[house_id][0] < record_date):
                    total_on_sale_info[house_id] = [record_date, house_size, total_price, unit_price]

            total_on_sale_unit_price, total_on_sale_total_price, total_on_sale_house_size = 0.0, 0.0, 0.0
            for house_id in total_on_sale_info.keys():
                total_on_sale_house_size = total_on_sale_house_size + total_on_sale_info[house_id][1]
                total_on_sale_total_price = total_on_sale_total_price + total_on_sale_info[house_id][2]
                total_on_sale_unit_price = total_on_sale_unit_price + total_on_sale_info[house_id][-1]

            if len(total_on_sale_info) != 0:
                total_on_sale_unit_price = round(total_on_sale_unit_price / len(total_on_sale_info), 2)
                total_on_sale_unit_price_per_size = round(total_on_sale_total_price / total_on_sale_house_size * 10000, 2)
            else:
                total_on_sale_unit_price = None
                total_on_sale_unit_price_per_size = None
            community_info.total_on_sale_unit_price = total_on_sale_unit_price
            community_info.total_on_sale_unit_price_per_size = total_on_sale_unit_price_per_size

            self.logger.info('community[{0}] total on sale info[{1}].'.format(community, total_on_sale_info))
            self.logger.info('community[{0}] total on sale unit price[{1}].'.format(community, total_on_sale_unit_price))
            self.logger.info('community[{0}] total on sale unit price per size[{1}].'.format(community, total_on_sale_unit_price_per_size))

            new_sold_info = self.sql_helper.get_community_new_sold_unit_price(city, community, time_begin, time_end)
            self.logger.info('community[{0}] new sold info[{1}].'.format(community, new_sold_info))
            if new_sold_info[0] != 0:
                community_info.new_sold_unit_price = new_sold_info[1]
                community_info.new_sold_unit_price_per_size = round(new_sold_info[2] / new_sold_info[3] * 10000, 2)
                community_info.new_sold_time_span = new_sold_info[4]

            self.sql_helper.insert_community_dynamic_info(community_info)
            pass
