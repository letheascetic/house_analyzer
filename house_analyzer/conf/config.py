# coding: utf-8

import logging


LOG_CONFIG = {
    'LOG_DIR': 'log/',
    'LOG_FILE_SIZE': 20*1024*1024,
    'LOG_FILE_BACKUP_COUNT': 5,
    'LOG_LEVER': logging.DEBUG,
    'LOG_FORMAT': logging.Formatter('[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(process)d][%(thread)d][%(message)s]')
}


MYSQL_CONFIG_TESTING = {
    'DB_CONNECT_TYPE': 'sqlalchemy',
    'DB_CONNECT_STRING': 'mysql+pymysql://ascetic:ascetic@127.0.0.1:3306/houseprice?charset=utf8mb4'
}


MYSQL_CONFIG_PRODUCTION = {
    'DB_CONNECT_TYPE': 'sqlalchemy',
    'DB_CONNECT_STRING': 'mysql+pymysql://ascetic:ascetic@101.132.173.34:3306/houseprice?charset=utf8mb4'
}


HOUSE_STATUS = {
    'ON_SALE': 1,
    'OFF_SALE': 2,
    'ON_SALE_OTHER': 3,
    'DEAL': 4,
    'DEAL_OTHER': 5
}

HOUSE_STATUS_SALE = [
    HOUSE_STATUS['ON_SALE'],
    HOUSE_STATUS['OFF_SALE'],
    HOUSE_STATUS['ON_SALE_OTHER']
]

HOUSE_STATUS_DEAL = [
    HOUSE_STATUS['DEAL'],
    HOUSE_STATUS['DEAL_OTHER'],
]
