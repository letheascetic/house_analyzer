# coding: utf-8


import json
import logging

from utils import util
from conf import config
from mysql.sqlhl import SqlHl
from mysql.base import HlHouseDynamicInfo


class MergeTool:
    """merge old db data to new db schema"""
    def __init__(self):
        self._init_logger()
        self.sql_helper = SqlHl(config.MYSQL_CONFIG)
        pass

    def _init_logger(self):
        util.config_logger()
        self.logger = logging.getLogger(__name__)

    def merge(self):
        for house in self.sql_helper.get_hl_data():
            history_price = {}
            if house.history_price is not None:
                history_price = json.loads(house.history_price)
            if house.list_date is not None and house.list_total_price is not None:
                history_price[house.list_date] = [house.list_total_price, round(house.list_total_price / house.house_size * 10000, 2)]
            if house.deal_date is not None and house.deal_total_price is not None and house.deal_unit_price is not None:
                history_price[house.deal_date] = [house.deal_total_price, house.deal_unit_price]
            self.logger.info('house[{0}] info: [{1}].'.format(house.house_id, history_price))

            for record_date, price in history_price.items():
                self.sql_helper.insert_or_update_house_dynamic_info(house.house_id, record_date, price)
