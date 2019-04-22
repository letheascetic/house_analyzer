# coding: utf-8

import logging
from sqlalchemy.ext.declarative import declarative_base

from homelink.db.base import HomeLink
from homelink.db.sqlutil import ISqlHelper


_Base = declarative_base()
logger = logging.getLogger(__name__)


class SqlHomeLink(ISqlHelper):
    """sql helper for home_link"""

    def __init__(self, config):
        super(SqlHomeLink, self).__init__(config)

    def insert(self, item):
        try:
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
                list_date=item['list_date'],
                last_trading_date=item['last_trading_date']
            )
            return self.add(row)
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
            row.total_price = item['total_price']
            row.unit_price = item['unit_price']
            row.room_info = item['room_info']
            row.floor_info = item['floor_info']
            row.orientation = item['orientation']
            row.decoration = item['decoration']
            row.house_size = item['house_size']
            row.house_type = item['house_type']
            row.community = item['community']
            row.district = item['district']
            row.location = item['location']
            row.room_structure = item['room_structure']
            row.room_size = item['room_size']
            row.building_structure = item['building_structure']
            row.elevator_household_ratio = item['elevator_household_ratio']
            row.elevator_included = item['elevator_included']
            row.property_right_deadline = item['property_right_deadline']
            row.list_date = item['list_date']
            row.last_trading_date = item['last_trading_date']

            self.session.commit()
            return True
        except Exception as e:
            logger.exception('update item[{0}] exception[{1}]'.format(item, e))
            self.session.rollback()
            return False
        finally:
            pass
