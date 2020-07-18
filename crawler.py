#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
from crawlers.DoubanGroupsCrawler import DoubanGroupsCrawler
from crawlers.DoubanGroupDiscussionsCrawler import DoubanGroupDiscussionsCrawler
import json
import os
from filters.Filter import Filter
import re
import argparse
import logging
import sys
from structs import DoubanGroup
from constants import LOGGER_FORMAT, CRAWLER_TYPE, CHROME_DRIVE_PATH

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--type", help="The web page to crawl, for example, douban_group_list", required=True
    )
    parser.add_argument(
        "--limit", help="The limit of processing pages", required=False, type=int
    )
    return parser.parse_args()


CRAWLER_FOLDER = "data/crawler"
FILTER_FOLDER = "data/filter/"


# TODO: fix the structure for all obj such as group/discussion
if __name__ == "__main__":
    args = get_args()
    logger.info(args)
    max_pages = args.limit if args.limit else sys.maxsize

    if args.type == CRAWLER_TYPE.DOUBAN_GROUP_LIST:
        # TODO: move constants to configs.py
        browser = webdriver.Chrome(CHROME_DRIVE_PATH)
        SHENZHEN_HOURSE_GROUP_LIST_URL = "https://www.douban.com/group/search?cat=1019&q=%E6%B7%B1%E5%9C%B3+%E7%A7%9F%E6%88%BF"
        SAVED_FILE_NAME = "深圳租房Groups.txt"

        crawler = DoubanGroupsCrawler(SHENZHEN_HOURSE_GROUP_LIST_URL, browser, max_pages=max_pages)
        crawler.start()
        browser.close()
        crawler.save(f"{CRAWLER_FOLDER}/{args.type}", SAVED_FILE_NAME)
    elif args.type == CRAWLER_TYPE.DOUBAN_DISCUSSION_LIST:
        # TODO: move constants to configs.py
        browser = webdriver.Chrome(CHROME_DRIVE_PATH)
        FILTER_DOUBAN_GROUP_LIST_FOLDER = FILTER_FOLDER + CRAWLER_TYPE.DOUBAN_GROUP_LIST + "/"
        ALLOWLIST_FILE_NAME = "深圳租房Groups_allowlist.txt"
        with open(FILTER_DOUBAN_GROUP_LIST_FOLDER + ALLOWLIST_FILE_NAME) as json_file:
            groups = [DoubanGroup._make(group) for group in json.load(json_file)]
        logger.info(f"total group count: {len(groups)}")
        for group in groups:
            link = group.link
            id_ = group.id
            discussions_crawler = DoubanGroupDiscussionsCrawler(
                url=f"{link}/discussion",
                group_id=id_,
                browser=browser,
                max_pages=max_pages,
            )
            discussions_crawler.start()
        browser.close()
