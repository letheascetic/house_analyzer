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

        sql_helper.insert_or_update_house_basic_info(item)
        sql_helper.insert_or_update_house_dynamic_info(item)

        return item
