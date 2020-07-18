#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
from filters.Filter import Filter
from filters.SingleFileFilter import SingleFileFilter
import re
import argparse
import logging
from constants import LOGGER_FORMAT, CRAWLER_TYPE, CRAWLER_FOLDER, FILTER_FOLDER
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)


def test_filter():
    path = os.getcwd() + "/data/discussions/"
    filter_ = Filter(path)
    filter_.start()


def print_discussion(file_path):
    with open(file_path) as json_file:
        discussion = json.load(json_file)
    print(discussion)


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type", help="The format of the data to be filtered, for example, douban_group_list", required=True
    )
    parser.add_argument(
        "--limit", help="The limit of output result", required=False, type=int
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

    if args.type == CRAWLER_TYPE.DOUBAN_GROUP_LIST:
        # TODO: move constants to constants.py/configs.py
        SAVED_FILE_NAME = "深圳租房Groups.txt"
        ALLOWLIST_FILE_NAME = "深圳租房Groups_allowlist.txt"
        CRAWLER_DOUBAN_GROUP_LIST_FOLDER = CRAWLER_FOLDER + "douban_group_list/"
        FILTER_DOUBAN_GROUP_LIST_FOLDER = FILTER_FOLDER + "douban_group_list/"
        limit = args.limit if args.limit else 50
        filter_ = SingleFileFilter(
            CRAWLER_DOUBAN_GROUP_LIST_FOLDER,
            SAVED_FILE_NAME,
            limit=limit,
        )
        filter_.start()
        if args.save:
            filter_.save(FILTER_DOUBAN_GROUP_LIST_FOLDER, ALLOWLIST_FILE_NAME)
    elif args.type == CRAWLER_TYPE.DOUBAN_DISCUSSION_LIST:
        DATA_FOLDER = CRAWLER_FOLDER + CRAWLER_TYPE.DOUBAN_DISCUSSION_LIST + "/"
        filter_ = Filter(DATA_FOLDER)
        filter_.start()
