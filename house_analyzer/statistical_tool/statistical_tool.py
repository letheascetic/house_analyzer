# coding: utf-8


import logging
import datetime

from utils import util
from conf import config
from mysql.sqlhl import SqlHl
from mysql.base import HlCommunityStatisticalInfo


class StatisticalTool:

    statistical_dates = None
    statistics_total_on_sale_price_after = '2019-05'

    def __init__(self):
        self._init_logger()
        self.sql_helper = SqlHl(config.MYSQL_CONFIG_PRODUCTION)
        self._init_paras()
        pass

    def _init_logger(self):
        # util.config_logger()
        self.logger = logging.getLogger(__name__)

    def _init_paras(self):
        today = datetime.datetime.utcnow()
        statistical_begin = datetime.datetime.strptime('2016-06', "%Y-%m")
        if today.month == 1:
            statistical_end = datetime.datetime(today.year - 1, 12, 1)
        else:
            statistical_end = datetime.datetime(today.year, today.month - 1, 1)

        self.statistical_dates = set()
        statistical_date = statistical_begin
        while statistical_date <= statistical_end:
            self.statistical_dates.add(statistical_date.strftime("%Y-%m"))
            if statistical_date.month == 12:
                statistical_date = datetime.datetime(statistical_date.year+1, 1, 1)
            else:
                statistical_date = datetime.datetime(statistical_date.year, statistical_date.month+1, 1)

    def do_statistics(self):

        for city, community in self.sql_helper.get_all_communities():
            all_statistical_dates = self.sql_helper.get_community_all_statistical_dates(city, community)
            all_statistical_dates = set([statistical_date[0] for statistical_date in all_statistical_dates])
            self.logger.info('city[{0}] community[{1}] old statistical dates[{2}]'.format(city, community, all_statistical_dates))

            new_statistical_dates = self.statistical_dates.difference(all_statistical_dates)
            self.logger.info('city[{0}] community[{1}] new statistical dates[{2}]'.format(city, community, new_statistical_dates))

            for statistical_date in new_statistical_dates:
                self.logger.info('start to statistics city[{0}] community[{1}] date[{2}]'.format(city, community, statistical_date))
                statistical_month, this_month_first_day, next_month_first_day = self.get_statistical_date_relevant(statistical_date)
                community_info = HlCommunityStatisticalInfo(city=city, community=community, statistical_date=statistical_date)
                # community_info.total_on_sale, community_info.total_off_sale, community_info.total_sold = 0, 0, 0

                community_info.total_on_sale = self.sql_helper.get_community_total_on_sale(city, community, next_month_first_day.strftime('%Y-%m-%d'))
                community_info.total_off_sale = self.sql_helper.get_community_total_off_sale(city, community, next_month_first_day.strftime('%Y-%m-%d'))
                community_info.total_sold = self.sql_helper.get_community_total_sold(city, community, next_month_first_day.strftime('%Y-%m-%d'))
                self.logger.info('community[{0}] total on sale[{1}].'.format(community, community_info.total_on_sale))
                self.logger.info('community[{0}] total off sale[{1}].'.format(community, community_info.total_off_sale))
                self.logger.info('community[{0}] total sold[{1}].'.format(community, community_info.total_sold))

                new_on_sale = self.sql_helper.get_community_new_on_sale(city, community, this_month_first_day.strftime('%Y-%m-%d'), next_month_first_day.strftime('%Y-%m-%d'))
                self.logger.info('community[{0}] new on sale[{1}].'.format(community, new_on_sale))
                community_info.new_on_sale = new_on_sale

                new_off_sale = self.sql_helper.get_community_new_off_sale(city, community, this_month_first_day.strftime('%Y-%m-%d'), next_month_first_day.strftime('%Y-%m-%d'))
                self.logger.info('community[{0}] new off sale[{1}].'.format(community, new_off_sale))
                community_info.new_off_sale = new_off_sale

                new_sold = self.sql_helper.get_community_new_sold(city, community, this_month_first_day.strftime('%Y-%m-%d'), next_month_first_day.strftime('%Y-%m-%d'))
                self.logger.info('community[{0}] new sold[{1}].'.format(community, new_sold))
                community_info.new_sold = new_sold

                if statistical_date < self.statistics_total_on_sale_price_after:
                    community_info.total_on_sale_unit_price = None
                    community_info.total_on_sale_unit_price_per_size = None
                else:
                    total_on_sale_info = {}
                    for house_id, record_date, total_price, house_size, unit_price in \
                            self.sql_helper.get_community_total_on_sale_unit_price(city, community, next_month_first_day.strftime('%Y-%m-%d')):
                        if house_id not in total_on_sale_info.keys():
                            total_on_sale_info[house_id] = [record_date, total_price, house_size, unit_price]
                        elif house_id in total_on_sale_info.keys() and total_on_sale_info[house_id][0] < record_date:
                            total_on_sale_info[house_id] = [record_date, total_price, house_size, unit_price]

                    total_on_sale_unit_price, total_on_sale_total_price, total_on_sale_house_size = 0.0, 0.0, 0.0
                    for house_id in total_on_sale_info.keys():
                        total_on_sale_house_size = total_on_sale_house_size + total_on_sale_info[house_id][2]
                        total_on_sale_total_price = total_on_sale_total_price + total_on_sale_info[house_id][1]
                        total_on_sale_unit_price = total_on_sale_unit_price + total_on_sale_info[house_id][3]

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

                new_sold_info = self.sql_helper.get_community_new_sold_unit_price(
                    city, community, this_month_first_day.strftime('%Y-%m-%d'), next_month_first_day.strftime('%Y-%m-%d'))
                self.logger.info('community[{0}] new sold info[{1}].'.format(community, new_sold_info))

                community_info.new_sold_unit_price = new_sold_info[1]
                community_info.new_sold_time_span = new_sold_info[4]
                if new_sold_info[0] == 0:
                    community_info.new_sold_unit_price_per_size = None
                else:
                    community_info.new_sold_unit_price_per_size = round(new_sold_info[2] / new_sold_info[3] * 10000, 2)

                self.sql_helper.insert_community_statistical_info(community_info)

    def get_statistical_date_relevant(self, statistical_date):
        statistical_month = datetime.datetime.strptime(statistical_date, "%Y-%m")
        this_month_first_day = datetime.datetime(statistical_month.year, statistical_month.month, 1)
        if statistical_month.month == 12:
            next_month_first_day = datetime.datetime(statistical_month.year + 1, 1, 1)
        else:
            next_month_first_day = datetime.datetime(statistical_month.year, statistical_month.month + 1, 1)
        return statistical_month, this_month_first_day, next_month_first_day
