# coding: utf-8

import logging
from sqlalchemy.ext.declarative import declarative_base

from conf import config
from sqlalchemy import func
from mysql.sqlutil import ISqlHelper
from mysql.base import HlHouseBasicInfo
from mysql.base import HlHouseDynamicInfo
from mysql.base import HlCommunityDynamicInfo


_Base = declarative_base()
logger = logging.getLogger(__name__)


class SqlHl(ISqlHelper):
    """sql helper for home_link"""

    def __init__(self, config):
        super(SqlHl, self).__init__(config)

    def query_house_basic_info(self, item):
        try:
            query = self.session.query(HlHouseBasicInfo).filter(HlHouseBasicInfo.house_id == item['house_id'])
            return query.first()
        except Exception as e:
            logger.exception('query house basic info[{0}] exception[{1}]'.format(item, e))

    def insert_or_update_house_basic_info(self, item):
        try:
            row = self.query_house_basic_info(item)
            if row is None:
                logger.info('new house info[{0}].'.format(item['house_id']))
                if item['status'] in config.HOUSE_STATUS_SALE:
                    row = HlHouseBasicInfo(
                        house_id=item['house_id'],
                        city=item['city'],
                        room_info=item['room_info'],
                        floor_info=item['floor_info'],
                        orientation=item['orientation'],
                        decoration=item['decoration'],
                        house_size=item['house_size'],
                        house_type=item['house_type'],
                        community=item['community'],
                        district=item['district'],
                        location=item['location'],
                        subway_info=item['subway_info'],
                        room_structure=item['room_structure'],
                        room_size=item['room_size'],
                        building_structure=item['building_structure'],
                        elevator_household_ratio=item['elevator_household_ratio'],
                        elevator_included=item['elevator_included'],
                        property_right_deadline=item['property_right_deadline'],
                        last_trading_date=item['last_trading_date'],
                        status=item['status'],
                        list_date=item['list_date'],
                    )
                else:
                    row = HlHouseBasicInfo(
                        house_id=item['house_id'],
                        city=item['city'],
                        status=item['status'],
                        deal_date=item['deal_date'],
                        deal_total_price=item['deal_total_price'],
                        deal_unit_price=item['deal_unit_price'],
                        deal_time_span=item['deal_time_span'],
                        list_total_price=item['list_total_price'],
                        list_unit_price=item['list_unit_price'],
                        price_change_times=item['price_change_times'],
                        community=item['community'],
                        room_info=item['room_info'],
                        district=item['district'],
                        location=item['location'],
                        house_size=item['house_size'],
                        list_date=item['list_date']
                    )
                return self.add(row)
            else:
                logger.info('old house info[{0}].'.format(item['house_id']))
                if row.status in config.HOUSE_STATUS_SALE and item['status'] in config.HOUSE_STATUS_DEAL:
                    logger.info('house[{0}] status change: [{1}] to [{2}].'.format(row.house_id, row.status, item['status']))
                    row.deal_date = item['deal_date']
                    row.deal_total_price = item['deal_total_price']
                    row.deal_unit_price = item['deal_unit_price']
                    row.deal_time_span = item['deal_time_span']
                    row.list_total_price = item['list_total_price']
                    row.list_unit_price = item['list_unit_price']
                    row.price_change_times = item['price_change_times']

                if row.status != item['status']:
                    logger.info('house[{0}] status change: [{1}] to [{2}].'.format(row.house_id, row.status, item['status']))
                    row.status = item['status']

                self.session.commit()
            return row
        except Exception as e:
            self.session.rollback()
            logger.exception('insert or update house basic info[{0}] exception[{1}].'.format(item, e))

    def get_house_id_list(self, city, house_status):
        try:
            query = self.session.query(HlHouseBasicInfo.house_id).filter(HlHouseBasicInfo.status == house_status)\
                .filter(HlHouseBasicInfo.city == city)
            return query.all()
        except Exception as e:
            logger.exception('get house id list exception[{0}]'.format(e))

    def get_house_id_list_v2(self):
        try:
            sql = "SELECT DISTINCT(house_id) FROM hl_house_dynamic_info WHERE house_id NOT IN (SELECT house_id FROM hl_house_basic_info) "
            query = self.session.execute(sql)
            # query = self.session.query(distinct(HlHouseDynamicInfo.house_id))
            # return query.all()
            return query.fetchall()
        except Exception as e:
            logger.exception('get house id list v2 exception[{0}]'.format(e))

    def query_house_dynamic_info(self, house_id, record_date):
        try:
            query = self.session.query(HlHouseDynamicInfo).filter(HlHouseDynamicInfo.house_id == house_id).filter(HlHouseDynamicInfo.record_date == record_date)
            return query.first()
        except Exception as e:
            logger.exception('query house dynamic info[{0}:{1}] exception[{2}]'.format(house_id, record_date, e))

    def query_newest_house_dynamic_info(self, house_id):
        try:
            query = self.session.query(HlHouseDynamicInfo).filter(HlHouseDynamicInfo.house_id == house_id)\
                .order_by(HlHouseDynamicInfo.record_date.desc())
            return query.first()
        except Exception as e:
            logger.exception('query house dynamic info[{0}] exception[{1}]'.format(house_id, e))

    def insert_or_update_house_dynamic_info(self, house_id, record_date, price):
        try:
            total_price, unit_price = price
            dynamic_info = self.query_newest_house_dynamic_info(house_id)

            if dynamic_info is None:
                logger.info('new house[{0}] dynamic info[{1}|{2}]'.format(house_id, record_date, price))
                new_dynamic_info = HlHouseDynamicInfo(
                    house_id=house_id,
                    record_date=record_date,
                    total_price=total_price,
                    unit_price=unit_price
                )
                self.session.add(new_dynamic_info)
            elif dynamic_info.record_date != record_date:
                if dynamic_info.total_price != total_price:
                    logger.info('house[{0}] dynamic info update from [{1}|{2}] to [{3}|{4}]'.format(
                        house_id, dynamic_info.record_date, (dynamic_info.total_price, dynamic_info.unit_price), record_date, price))
                    new_dynamic_info = HlHouseDynamicInfo(
                        house_id=house_id,
                        record_date=record_date,
                        total_price=total_price,
                        unit_price=unit_price
                    )
                    self.session.add(new_dynamic_info)
            else:
                if dynamic_info.total_price != total_price:
                    logger.info('house[{0}] dynamic info update from [{1}|{2}] to [{3}|{4}]'.format(
                        house_id, dynamic_info.record_date, (dynamic_info.total_price, dynamic_info.unit_price), record_date, price))
                    dynamic_info.total_price = total_price
                    dynamic_info.unit_price = unit_price
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            logger.exception('insert or update house dynamic info[{0}:{1}:{2}] exception[{3}]'.format(house_id, record_date, price, e))

    def get_all_house_basic_info(self):
        try:
            query = self.session.query(HlHouseBasicInfo)
            return query.all()
        except Exception as e:
            logger.exception('get all house basic info exception[{0}]'.format(e))

    def get_all_house_dynamic_info(self):
        try:
            query = self.session.query(HlHouseDynamicInfo)
            return query.all()
        except Exception as e:
            logger.exception('get all house dynamic info exception[{0}]'.format(e))

    def get_all_communities(self):
        try:
            query = self.session.query(HlHouseBasicInfo.city, HlHouseBasicInfo.community)\
                .group_by(HlHouseBasicInfo.community, HlHouseBasicInfo.city)
            return query.all()
        except Exception as e:
            logger.exception('get all communities exception[{0}]'.format(e))

    def get_community_total_status(self, city, community):
        try:
            query = self.session.query(HlHouseBasicInfo.status, func.count('*'))\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .group_by(HlHouseBasicInfo.status)
            return query.all()
        except Exception as e:
            logger.exception('get community[{0}:{1}] total status exception[{2}]'.format(city, community, e))

    def get_community_new_on_sale(self, city, community, time_begin, time_end):
        try:
            query = self.session.query(func.count('1'))\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .filter(HlHouseBasicInfo.status == config.HOUSE_STATUS['ON_SALE'])\
                .filter(HlHouseBasicInfo.list_date.between(time_begin, time_end))
            return query.one()[0]
        except Exception as e:
            logger.exception('get community[{0}:{1}] new on sale exception[{2}]'.format(city, community, e))

    def get_community_new_off_sale(self, city, community, time_begin, time_end):
        try:
            query = self.session.query(func.count('1'))\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .filter(HlHouseBasicInfo.status == config.HOUSE_STATUS['OFF_SALE'])\
                .filter(HlHouseBasicInfo.update_time.between(time_begin, time_end))
            return query.one()[0]
        except Exception as e:
            logger.exception('get community[{0}:{1}] new off sale exception[{2}]'.format(city, community, e))

    def get_community_new_sold(self, city, community, time_begin, time_end):
        try:
            query = self.session.query(func.count('1'))\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .filter(HlHouseBasicInfo.status == config.HOUSE_STATUS['DEAL'])\
                .filter(HlHouseBasicInfo.deal_date.between(time_begin, time_end))
            return query.one()[0]
        except Exception as e:
            logger.exception('get community[{0}:{1}] new sold exception[{2}]'.format(city, community, e))

    def get_community_total_on_sale_unit_price(self, city, community):
        try:
            query = self.session.query(HlHouseBasicInfo.house_id, HlHouseBasicInfo.house_size,
                                       HlHouseDynamicInfo.record_date, HlHouseDynamicInfo.total_price,
                                       HlHouseDynamicInfo.unit_price)\
                .join(HlHouseDynamicInfo, HlHouseBasicInfo.house_id == HlHouseDynamicInfo.house_id)\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .filter(HlHouseBasicInfo.status == config.HOUSE_STATUS['ON_SALE'])
            return query.all()
        except Exception as e:
            logger.exception('get community[{0}:{1}] total on sale unit price exception[{2}]'.format(city, community, e))

    def get_community_new_sold_unit_price(self, city, community, time_begin, time_end):
        try:
            query = self.session.query(func.count('1'), func.avg(HlHouseBasicInfo.deal_unit_price), func.sum(HlHouseBasicInfo.deal_total_price), func.sum(HlHouseBasicInfo.house_size), func.avg(HlHouseBasicInfo.deal_time_span))\
                .filter(HlHouseBasicInfo.city == city).filter(HlHouseBasicInfo.community == community)\
                .filter(HlHouseBasicInfo.status == config.HOUSE_STATUS['DEAL'])\
                .filter(HlHouseBasicInfo.deal_date.between(time_begin, time_end))
            return query.one()
        except Exception as e:
            logger.exception('get community[{0}:{1}] new sold unit price exception[{2}]'.format(city, community, e))

    def get_community_last_statistical_date(self, city, community):
        try:
            query = self.session.query(HlCommunityDynamicInfo.statistical_date)\
                .filter(HlCommunityDynamicInfo.city == city).filter(HlCommunityDynamicInfo.community == community)\
                .order_by(HlCommunityDynamicInfo.statistical_date.desc()).limit(1)
            if query.first():
                return query.first()[0]
            return None
        except Exception as e:
            logger.exception('get community[{0}:{1}] last statistical date exception[{2}]'.format(city, community, e))

    def insert_community_dynamic_info(self, community_info):
        try:
            self.add(community_info)
        except Exception as e:
            logger.exception('insert community dynamic info[{0}] exception[{1}].'.format(community_info, e))
