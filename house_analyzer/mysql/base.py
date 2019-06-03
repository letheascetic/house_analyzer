# coding:utf-8

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, VARCHAR, TEXT, INTEGER, BINARY, TIMESTAMP, SMALLINT, BIGINT, FLOAT, DATE


_Base = declarative_base()


class HomeLink(_Base):
    """class for home_link"""
    __tablename__ = 'home_link'

    house_id = Column('house_id', VARCHAR(64), primary_key=True, unique=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    total_price = Column('total_price', FLOAT, index=True, nullable=False)
    unit_price = Column('unit_price', FLOAT, index=True, nullable=False)
    room_info = Column('room_info', VARCHAR(64), default=None, nullable=True)
    floor_info = Column('floor_info', VARCHAR(64), default=None, nullable=True)
    orientation = Column('orientation', VARCHAR(64), default=None, nullable=True)
    decoration = Column('decoration', VARCHAR(64), default=None, nullable=True)
    house_size = Column('house_size', FLOAT, index=True, default=None, nullable=True)
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
    last_trading_date = Column('last_trading_date', VARCHAR(64), index=True, default=None, nullable=True)
    create_time = Column('create_time', TIMESTAMP, default=datetime.datetime.utcnow, index=True)
    update_time = Column('update_time', TIMESTAMP, default=None, index=True, onupdate=datetime.datetime.utcnow)
    history_price = Column('history_price', VARCHAR(2048), default=None)
    status = Column('status', INTEGER, default=1)
    list_date = Column('list_date', VARCHAR(64), index=True, default=None, nullable=True)
    list_total_price = Column('list_total_price', FLOAT, default=None, nullable=True)
    deal_date = Column('deal_date', VARCHAR(64), index=True, default=None, nullable=True)
    deal_total_price = Column('deal_total_price', FLOAT, default=None, nullable=True)
    deal_unit_price = Column('deal_unit_price', FLOAT, default=None, nullable=True)
    deal_time_span = Column('deal_time_span', INTEGER, default=None, nullable=True)
    price_change_times = Column('price_change_times', INTEGER, default=None, nullable=True)


class HlHouseBasicInfo(_Base):
    """class for hl_house_basic_info"""
    __tablename__ = 'hl_house_basic_info'

    house_id = Column('house_id', VARCHAR(64), primary_key=True, unique=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    room_info = Column('room_info', VARCHAR(64), default=None, nullable=True)
    floor_info = Column('floor_info', VARCHAR(64), default=None, nullable=True)
    orientation = Column('orientation', VARCHAR(64), default=None, nullable=True)
    decoration = Column('decoration', VARCHAR(64), default=None, nullable=True)
    house_size = Column('house_size', FLOAT, index=True, default=None, nullable=True)
    house_type = Column('house_type', VARCHAR(64), index=True, default=None, nullable=True)
    community = Column('community', VARCHAR(64), index=True, nullable=False)
    district = Column('district', VARCHAR(64), index=True, nullable=False)
    location = Column('location', VARCHAR(64), index=True, nullable=False)
    subway_info = Column('subway_info', VARCHAR(256), index=True, nullable=False)
    room_structure = Column('room_structure', VARCHAR(64), default=None, nullable=True)
    room_size = Column('room_size', VARCHAR(64), default=None, nullable=True)
    building_structure = Column('building_structure', VARCHAR(64), default=None, nullable=True)
    elevator_household_ratio = Column('elevator_household_ratio', VARCHAR(64), default=None, nullable=True)
    elevator_included = Column('elevator_included', VARCHAR(64), default=None, nullable=True)
    property_right_deadline = Column('property_right_deadline', VARCHAR(64), default=None, nullable=True)
    last_trading_date = Column('last_trading_date', VARCHAR(64), index=True, default=None, nullable=True)
    create_time = Column('create_time', TIMESTAMP, default=datetime.datetime.utcnow, index=True)
    update_time = Column('update_time', TIMESTAMP, default=None, index=True, onupdate=datetime.datetime.utcnow)
    status = Column('status', INTEGER, default=1)
    list_date = Column('list_date', DATE, index=True, default=None, nullable=True)
    list_total_price = Column('list_total_price', FLOAT, default=None, nullable=True)
    list_unit_price = Column('list_unit_price', FLOAT, default=None, nullable=True)
    deal_date = Column('deal_date', DATE, index=True, default=None, nullable=True)
    deal_total_price = Column('deal_total_price', FLOAT, default=None, nullable=True)
    deal_unit_price = Column('deal_unit_price', FLOAT, default=None, nullable=True)
    deal_time_span = Column('deal_time_span', INTEGER, default=None, nullable=True)
    price_change_times = Column('price_change_times', INTEGER, default=None, nullable=True)


class HlHouseDynamicInfo(_Base):
    """class for hl_house_dynamic_info"""
    __tablename__ = 'hl_house_dynamic_info'

    id = Column('id', BIGINT, primary_key=True, autoincrement=True, unique=True, nullable=False)
    house_id = Column('house_id', VARCHAR(64), nullable=False, index=True)
    total_price = Column('total_price', FLOAT, index=True, nullable=False)
    unit_price = Column('unit_price', FLOAT, index=True, nullable=False)
    record_date = Column('record_date', DATE, index=True, default=None, nullable=False)
    update_time = Column('update_time', TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class HlCommunityStatisticalInfo(_Base):
    """class for hl_community_statistical_info"""

    __tablename__ = 'hl_community_statistical_info'

    id = Column('id', BIGINT, primary_key=True, autoincrement=True, nullable=False)
    community = Column('community', VARCHAR(64), index=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    statistical_date = Column('statistical_date', DATE, index=True, nullable=False)
    total_on_sale = Column('total_on_sale', INTEGER, nullable=False)
    total_off_sale = Column('total_off_sale', INTEGER, nullable=False)
    total_sold = Column('total_sold', INTEGER, nullable=False)
    new_on_sale = Column('new_on_sale', INTEGER, nullable=False)
    new_off_sale = Column('new_off_sale', INTEGER, nullable=False)
    new_sold = Column('new_sold', INTEGER, nullable=False)
    total_on_sale_unit_price = Column('total_on_sale_unit_price', FLOAT, nullable=False)
    total_on_sale_unit_price_per_size = Column('total_on_sale_unit_price_per_size', FLOAT, nullable=False)
    new_sold_unit_price = Column('new_sold_unit_price', FLOAT, nullable=False)
    new_sold_unit_price_per_size = Column('new_sold_unit_price_per_size', FLOAT, nullable=False)
    new_sold_time_span = Column('new_sold_time_span', FLOAT, nullable=False)
    update_time = Column('update_time', TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class HlCommunityBasicInfo(_Base):
    """class for hl_community_basic_info"""

    __tablename__ = 'hl_community_basic_info'

    community_id = Column('community_id', VARCHAR(64), primary_key=True, nullable=False)
    community = Column('community', VARCHAR(64), index=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    address = Column('address', VARCHAR(256), nullable=True)
    architectural_age = Column('architectural_age', VARCHAR(64), nullable=True)
    architectural_type = Column('architectural_type', VARCHAR(64), nullable=True)
    property_costs = Column('property_costs', VARCHAR(64), nullable=True)
    property_company = Column('property_company', VARCHAR(64), nullable=True)
    developer = Column('developer', VARCHAR(64), nullable=True)
    total_buildings = Column('total_buildings', VARCHAR(64), nullable=True)
    total_houses = Column('total_houses', VARCHAR(64), nullable=True)
    district = Column('district', VARCHAR(64), nullable=True)
    location = Column('location', VARCHAR(64), nullable=True)
    subway_info = Column('subway_info', VARCHAR(256), nullable=True)
    update_time = Column('update_time', TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class HlCommunityDynamicInfo(_Base):
    """class for hl_community_dynamic_info"""

    __tablename__ = 'hl_community_dynamic_info'

    id = Column('id', BIGINT, primary_key=True, autoincrement=True, nullable=False)
    community = Column('community', VARCHAR(64), index=True, nullable=False)
    city = Column('city', VARCHAR(64), index=True, nullable=False)
    record_date = Column('record_date', DATE, index=True, default=None, nullable=False)
    sold_recently = Column('sold_recently', INTEGER, nullable=True)
    on_sale = Column('on_sale', INTEGER, nullable=True)
    unit_price = Column('unit_price', FLOAT, nullable=True)
    update_time = Column('update_time', TIMESTAMP, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
