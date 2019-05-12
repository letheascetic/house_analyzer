# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HomelinkItem(scrapy.Item):
    # define the fields for your item here like:

    # 必填项
    url = scrapy.Field()            # 爬取数据的网页
    house_id = scrapy.Field()       # 房屋编号
    city = scrapy.Field()           # 所在城市

    # 在售房源相关数据 - 主信息
    total_price = scrapy.Field()    # 当前总价
    unit_price = scrapy.Field()     # 当前单价
    room_info = scrapy.Field()      # 户型，如：1室1厅
    floor_info = scrapy.Field()     # 楼层信息，如：低楼层/共6层
    orientation = scrapy.Field()    # 朝向，如：南 北
    decoration = scrapy.Field()     # 装修
    house_size = scrapy.Field()     # 房屋大小
    house_type = scrapy.Field()     # 房屋类型（板楼、塔楼）
    community = scrapy.Field()      # 所在小区（聚银时代）
    district = scrapy.Field()       # 所在区（柯桥区）
    location = scrapy.Field()       # 所在区位置（柯北）

    # 在售房源相关数据 - 基本信息（基本属性）
    room_structure = scrapy.Field()         # 户型结构（平层、暂无数据）
    room_size = scrapy.Field()              # 套内面积
    building_structure = scrapy.Field()     # 建筑结构（钢混结构、框架结构）
    elevator_household_ratio = scrapy.Field()   # 电梯户数比例
    elevator_included = scrapy.Field()          # 是否有电梯
    property_right_deadline = scrapy.Field()    # 产权年限

    # 在售房源相关数据 - 基本信息（交易属性）
    list_date = scrapy.Field()          # 挂牌时间（上架时间）
    last_trading_date = scrapy.Field()  # 上次交易时间

    # 必填项，自定义的数据
    status = scrapy.Field()             # 房屋状态：1-在售，2-在售下架，3-在售其他，4-成交，5-成交其他情况

    # 成交房源相关信息 - 主信息
    deal_date = scrapy.Field()              # 成交时间
    deal_total_price = scrapy.Field()       # 成交总价
    deal_unit_price = scrapy.Field()        # 成交单价
    deal_time_span = scrapy.Field()         # 成交周期（天）
    list_total_price = scrapy.Field()       # 挂牌总价
    list_unit_price = scrapy.Field()
    price_change_times = scrapy.Field()     # 调价次数

    pass
