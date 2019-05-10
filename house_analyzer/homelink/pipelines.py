# -*- coding: utf-8 -*-

import logging
from scrapy.exceptions import DropItem


logger = logging.getLogger(__name__)


class FilterPipeline(object):
    def process_item(self, item, spider):
        logger.info('process item[{0}] in filter pipeline'.format(item))

        sql_helper = getattr(spider, 'sql_helper', None)
        if not sql_helper:
            raise DropItem('sql helper is None: [{0}]'.format(item))

        row = sql_helper.query(item)
        if row is not None:
            logger.info('update old item[{0}].'.format(item))
            sql_helper.update(row, item)
        else:
            logger.info('insert new item[{0}].'.format(item))
            sql_helper.insert(item)
        return item
