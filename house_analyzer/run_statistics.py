# coding: utf-8

from utils import util
from statistical_tool.statistical_tool import StatisticalTool


if __name__ == "__main__":
    util.config_logger()
    statistical_tool = StatisticalTool()
    statistical_tool.do_statistics()
    pass

