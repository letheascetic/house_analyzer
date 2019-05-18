# coding: utf-8

from utils import util
from homelink.spiders.sx import SxSpider
from homelink.spiders.hz import HzSpider
from homelink.spiders.nj import NjSpider
from homelink.spiders.nj2 import Nj2Spider
from homelink.spiders.hz2 import Hz2Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


if __name__ == '__main__':
    util.config_logger()
    process = CrawlerProcess(get_project_settings())
    process.crawl(SxSpider)
    process.crawl(HzSpider)
    process.crawl(NjSpider)
    process.crawl(Nj2Spider)
    process.crawl(Hz2Spider)
    process.start()
    pass


