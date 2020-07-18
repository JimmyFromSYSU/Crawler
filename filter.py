#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 卓越时代广场：https://ditu.amap.com/dir?from%5Bid%5D=BV10243512-from&from%5Bname%5D=%E7%A6%8F%E7%94%B0%E5%8F%A3%E5%B2%B8(%E5%9C%B0%E9%93%81%E7%AB%99)&from%5Blnglat%5D=114.069273%2C22.515737&from%5Bmodxy%5D=114.069273%2C22.515737&from%5Bpoitype%5D=150500&from%5Badcode%5D=440304&to%5Bname%5D=%E5%8D%93%E8%B6%8A%C2%B7%E6%97%B6%E4%BB%A3%E5%B9%BF%E5%9C%BA&to%5Blnglat%5D=114.057131%2C22.534121&to%5Bid%5D=B02F37T14X-to&to%5Bpoitype%5D=120201&to%5Badcode%5D=440300&to%5Bmodxy%5D=114.057252%2C22.534603&type=bus&policy=0&dateTime=now

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
from filters.Filter import Filter
from filters.SingleFileFilter import SingleFileFilter
import re
import argparse
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(name)s/%(levelname)s: %(message)s')


def test_filter():
    path = os.getcwd() + "/data/discussions/"
    filter_ = Filter(path)
    filter_.start()


def print_discussion(file_path):
    with open(file_path) as json_file:
        discussion = json.load(json_file)
    print(discussion)


# save_all_groups()

# save_whitelist_groups()
# print_whitelist_groups()

# test_single_discussion_page()
# print_discussion("/Users/zhiliu/Desktop/script/crawler/data/discussions/106955/169763419")

# test_filter()
# save_all_discussions()


class DATA_FORMAT:
    DOUBAN_GROUP_LIST =  'douban_group_list'
    DOUBAN_DISCUSSION_LIST = 'douban_discussion_list'


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format", help="The format of the data to be filtered, for example, douban_group_list", required=True
    )
    parser.add_argument(
        "--save",
        help="Save the filtered resultr",
        required=False,
        action="store_true",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    logger.info(args)

    if args.format == DATA_FORMAT.DOUBAN_GROUP_LIST:
        # TODO: move constants to configs.py
        SAVED_FILE_NAME = "深圳租房Groups.txt"
        ALLOWLIST_FILE_NAME = "深圳租房Groups_allowlist.txt"
        CRAWLER_FOLDER = "data/crawler/"
        FILTER_FOLDER = "data/filter/"
        CRAWLER_DOUBAN_GROUP_LIST_FOLDER = CRAWLER_FOLDER + "douban_group_list/"
        FILTER_DOUBAN_GROUP_LIST_FOLDER = FILTER_FOLDER + "douban_group_list/"
        filter_ = SingleFileFilter(
            CRAWLER_DOUBAN_GROUP_LIST_FOLDER,
            SAVED_FILE_NAME,
            limit=50,
        )
        filter_.start()
        if args.save:
            filter_.save(FILTER_DOUBAN_GROUP_LIST_FOLDER, ALLOWLIST_FILE_NAME)
