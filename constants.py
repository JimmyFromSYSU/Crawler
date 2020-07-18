#!/usr/bin/python
# -*- coding: UTF-8 -*-

LOGGER_FORMAT = '[%(asctime)s] %(message)s'
CRAWLER_FOLDER = "data/crawler/"
FILTER_FOLDER = "data/filter/"
CHROME_DRIVE_PATH = "./bin/chromedriver"


class CRAWLER_TYPE:
    DOUBAN_GROUP_LIST =  'douban_group_list'
    DOUBAN_DISCUSSION_LIST = 'douban_discussion_list'
