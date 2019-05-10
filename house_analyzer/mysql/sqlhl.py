# coding: utf-8

import json
import logging
import datetime
from sqlalchemy.ext.declarative import declarative_base

from conf import config
from mysql.base import HomeLink
from mysql.sqlutil import ISqlHelper
from mysql.base import HlHouseBasicInfo
from mysql.base import HlHouseDynamicInfo


_Base = declarative_base()
logger = logging.getLogger(__name__)


class SqlHl(ISqlHelper):
    """sql helper for home_link"""

    def __init__(self, config):
        super(SqlHl, self).__init__(config)

    def insert(self, item):
        try:
            if item['status'] in config.HOUSE_STATUS_SALE:
                history = {}
                record_date = datetime.datetime.today().strftime('%Y-%m-%d')
                history[record_date] = [item['total_price'], item['unit_price']]

                row = HomeLink(
                    house_id=item['house_id'],
                    city=item['city'],
                    total_price=item['total_price'],
                    unit_price=item['unit_price'],
                    room_info=item['room_info'],
                    floor_info=item['floor_info'],
                    orientation=item['orientation'],
                    decoration=item['decoration'],
                    house_size=item['house_size'],
                    house_type=item['house_type'],
                    community=item['community'],
                    district=item['district'],
                    location=item['location'],
                    room_structure=item['room_structure'],
                    room_size=item['room_size'],
                    building_structure=item['building_structure'],
                    elevator_household_ratio=item['elevator_household_ratio'],
                    elevator_included=item['elevator_included'],
                    property_right_deadline=item['property_right_deadline'],
                    last_trading_date=item['last_trading_date'],
                    history_price=json.dumps(history),
                    status=item['status'],
                    list_date=item['list_date'],
                )
                return self.add(row)
            elif item['status'] in config.HOUSE_STATUS_DEAL:
                history = {}

                list_unit_price = round(item['list_total_price'] / item['house_size'] * 10000, 2)

                history[item['list_date']] = [item['list_total_price'], list_unit_price]
                history[item['deal_date']] = [item['deal_total_price'], item['deal_unit_price']]

                row = HomeLink(
                    house_id=item['house_id'],
                    city=item['city'],
                    status=item['status'],
                    deal_date=item['deal_date'],
                    deal_total_price=item['deal_total_price'],
                    deal_unit_price=item['deal_unit_price'],
                    deal_time_span=item['deal_time_span'],
                    list_total_price=item['list_total_price'],
                    price_change_times=item['price_change_times'],
                    history_price=json.dumps(history),

                    community=item['community'],
                    room_info=item['room_info'],
                    district=item['district'],
                    location=item['location'],
                    total_price=item['total_price'],
                    unit_price=item['unit_price'],
                    house_size=item['house_size'],
                    list_date=item['list_date']
                )
                return self.add(row)
            else:
                logger.warning('not matching url:[{0}]'.format(item['url']))
                return None
        except Exception as e:
            logger.exception('insert item[{0}] exception[{1}]'.format(item, e))

    def query(self, item):
        try:
            query = self.session.query(HomeLink).filter(HomeLink.house_id == item['house_id'])
            return query.first()
        except Exception as e:
            logger.exception('query item[{0}] exception[{1}]'.format(item, e))

    def update(self, row, item):
        try:
            if item['status'] in config.HOUSE_STATUS_SALE:
                history = None
                if row.history_price is None:  # 第一次未记录历史价格，则更新
                    history = {row.create_time.strftime('%Y-%m-%d'): [row.total_price, row.unit_price]}
                    row.history_price = json.dumps(history)

                if row.total_price != item['total_price']:
                    if history is None:
                        history = json.loads(row.history_price)
                    record_date = datetime.datetime.today().strftime('%Y-%m-%d')
                    history[record_date] = [item['total_price'], item['unit_price']]
                    row.history_price = json.dumps(history)
                    logger.info('house[{0}] price change[{1}].'.format(row.house_id, row.history_price))

                row.community = item['community']
                row.total_price = item['total_price']
                row.unit_price = item['unit_price']
                row.status = item['status']
                self.session.commit()
                return True
            elif item['status'] in config.HOUSE_STATUS_DEAL:
                if row.deal_date is None:
                    row.deal_date = item['deal_date']
                    row.deal_total_price = item['deal_total_price']
                    row.deal_unit_price = item['deal_unit_price']
                    row.deal_time_span = item['deal_time_span']
                    row.list_total_price = item['list_total_price']
                    row.price_change_times = item['price_change_times']

                    if row.history_price is None:
                        history = {}
                        list_date = datetime.datetime.strptime(item['deal_date'], "%Y-%m-%d") - datetime.timedelta(
                            days=item['deal_time_span'])
                        record_date = list_date.strftime('%Y-%m-%d')
                        house_size = round(item['deal_total_price'] / item['deal_unit_price'] * 10000, 2)
                        list_unit_price = round(item['list_total_price'] / house_size, 2)
                        history[record_date] = [item['list_total_price'], list_unit_price]
                        history[item['deal_date']] = [item['deal_total_price'], item['deal_unit_price']]
                    else:
                        history = json.loads(row.history_price)
                        history[item['deal_date']] = [item['deal_total_price'], item['deal_unit_price']]

                    row.history_price = json.dumps(history)

                row.community = item['community']
                row.room_info = item['room_info']
                row.district = item['district']
                row.location = item['location']
                row.total_price = item['total_price']
                row.unit_price = item['unit_price']
                row.house_size = item['house_size']
                row.list_date = item['list_date']

                row.status = item['status']
                self.session.commit()
                return True
            else:
                logger.warning('not matching url:[{0}]'.format(item['url']))
                return False
        except Exception as e:
            logger.exception('update item[{0}] exception[{1}]'.format(item, e))
            self.session.rollback()
            return False
        finally:
            pass

    def get_house_id_list(self, house_status):
        try:
            query = self.session.query(HomeLink.house_id).filter(HomeLink.status == house_status)
            return query.all()
        except Exception as e:
            logger.exception('get house id list exception[{0}]'.format(e))

    def get_hl_data(self):
        try:
            query = self.session.query(HomeLink)
            return query.all()
        except Exception as e:
            logger.exception('get homelink data exception[{0}]'.format(e))

    def query_house_dynamic_info(self, house_id, record_date):
        try:
            query = self.session.query(HlHouseDynamicInfo).filter(HlHouseDynamicInfo.house_id == house_id).filter(HlHouseDynamicInfo.record_date == record_date)
            return query.first()
        except Exception as e:
            logger.exception('query house dynamic info[{0}{1}] exception[{2}]'.format(house_id, record_date, e))

    def update_session(self):
        try:
            self.session.commit()
        except Exception as e:
            logger.exception('update exception[{0}]'.format(e))

    def insert_or_update_house_dynamic_info(self, house_id, record_date, price):
        try:
            total_price, unit_price = price
            query = self.session.query(HlHouseDynamicInfo).filter(HlHouseDynamicInfo.house_id == house_id).filter(HlHouseDynamicInfo.record_date == record_date)
            dynamic_info = query.first()
            if dynamic_info is not None:
                dynamic_info.total_price = total_price
                dynamic_info.unit_price = unit_price
            else:
                dynamic_info = HlHouseDynamicInfo(
                    house_id=house_id,
                    record_date=record_date,
                    total_price=total_price,
                    unit_price=unit_price
                )
                self.session.add(dynamic_info)
            self.session.commit()
        except Exception as e:
            logger.exception('insert or update house dynamic info[{0}:{1}:{2}] exception[{3}]'.format(house_id, record_date, price, e))
