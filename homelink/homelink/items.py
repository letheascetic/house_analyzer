# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HomelinkItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()           # 所在城市
    house_id = scrapy.Field()       # 房屋编号

    total_price = scrapy.Field()    # 总价
    unit_price = scrapy.Field()     # 单价

    room_info = scrapy.Field()      # 户型
    floor_info = scrapy.Field()     # 楼层信息

    orientation = scrapy.Field()    # 朝向
    decoration = scrapy.Field()     # 装修

    house_size = scrapy.Field()     # 房屋大小
    house_type = scrapy.Field()     # 房屋类型（板楼、塔楼）

    community = scrapy.Field()      # 所在小区
    district = scrapy.Field()       # 所在区（柯桥区）
    location = scrapy.Field()       # 所在区位置（柯北）

    room_structure = scrapy.Field()         # 户型结构
    room_size = scrapy.Field()              # 套内面积
    building_structure = scrapy.Field()     # 建筑结构（钢混结构）
    elevator_household_ratio = scrapy.Field()   # 电梯户数比例
    elevator_included = scrapy.Field()          # 是否有电梯
    property_right_deadline = scrapy.Field()    # 产权年限

    list_date = scrapy.Field()          # 挂牌时间
    last_trading_date = scrapy.Field()  # 上次交易时间

    pass
