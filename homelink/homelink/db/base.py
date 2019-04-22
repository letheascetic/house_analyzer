# coding:utf-8

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER, BINARY, TIMESTAMP, SMALLINT, BIGINT, FLOAT


_Base = declarative_base()


class HomeLink(_Base):
    """class for home_link"""
    __tablename__ = 'home_link_sx'

    house_id = Column('house_id', BIGINT, primary_key=True, autoincrement=True, unique=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    total_price = Column('total_price', FLOAT, index=True, nullable=False)
    unit_price = Column('unit_price', FLOAT, index=True, nullable=False)
    room_info = Column('room_info', VARCHAR(64), default=None, nullable=True)
    floor_info = Column('floor_info', VARCHAR(64), default=None, nullable=True)
    orientation = Column('orientation', VARCHAR(64), default=None, nullable=True)
    decoration = Column('decoration', VARCHAR(64), default=None, nullable=True)
    house_size = Column('house_size', VARCHAR(64), index=True, default=None, nullable=True)
    house_type = Column('house_type', VARCHAR(64), index=True, default=None, nullable=True)
    community = Column('community', VARCHAR(64), index=True, nullable=False)
    district = Column('district', VARCHAR(64), index=True, nullable=False)
    location = Column('location', VARCHAR(64), index=True, nullable=False)
    room_structure = Column('room_structure', VARCHAR(64), default=None, nullable=True)
    room_size = Column('room_size', VARCHAR(64), default=None, nullable=True)
    building_structure = Column('building_structure', VARCHAR(64), default=None, nullable=True)
    elevator_household_ratio = Column('elevator_household_ratio', VARCHAR(64), default=None, nullable=True)
    elevator_included = Column('elevator_included', VARCHAR(64), default=None, nullable=True)
    property_right_deadline = Column('property_right_deadline', VARCHAR(64), default=None, nullable=True)
    list_date = Column('list_date', VARCHAR(64), index=True, default=None, nullable=True)
    last_trading_date = Column('last_trading_date', VARCHAR(64), index=True, default=None, nullable=True)
    create_time = Column('create_time', TIMESTAMP, default=datetime.datetime.utcnow, index=True)
    update_time = Column('update_time', TIMESTAMP, default=None, index=True, onupdate=datetime.datetime.utcnow)