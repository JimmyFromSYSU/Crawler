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
from constants import LOGGER_FORMAT

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

CHROME_DRIVE_PATH = "./bin/chromedriver"

WHITELIST_DOUBAN_GROUPS_FILE = "douban_groups_whitelist.txt"


def test_single_discussion_page():
    group = {
        'name': '福田租房',
        'link': 'https://www.douban.com/group/586502',
        'id': '586502',
    }
    browser = webdriver.Chrome(CHROME_DRIVE_PATH)
    link = group['link']
    id_ = group['id']
    discussions_crawler = DoubanGroupDiscussionsCrawler(f"{link}/discussion", id_, browser)
    discussions_crawler.start()
    browser.close()


def save_all_discussions():
    with open(WHITELIST_DOUBAN_GROUPS_FILE) as json_file:
        groups = json.load(json_file)

    print(f"total count: {len(groups)}")

    browser = webdriver.Chrome(CHROME_DRIVE_PATH)
    for group in groups:
        link = group['link']
        id_ = group['id']
        discussions_crawler = DoubanGroupDiscussionsCrawler(f"{link}/discussion", id_, browser)
        discussions_crawler.start()
    browser.close()


def print_discussion(file_path):
    with open(file_path) as json_file:
        discussion = json.load(json_file)
    print(discussion)


class WEB_PAGE:
    DOUBAN_GROUP_LIST =  'douban_group_list'
    DOUBAN_DISCUSSION_LIST = 'douban_discussion_list'


def get_args() -> argparse.Namespace:
    logger.info("Parse arguments.")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--page", help="The web page to crawl, for example, douban_group_list", required=True
    )
    return parser.parse_args()


CRAWLER_FOLDER = "data/crawler"
FILTER_FOLDER = "data/filter/"


# TODO: fix the structure for all obj such as group/discussion
if __name__ == "__main__":
    args = get_args()
    logger.info(args)
    MAX_PAGES = sys.maxsize

    if args.page == WEB_PAGE.DOUBAN_GROUP_LIST:
        # TODO: move constants to configs.py
        browser = webdriver.Chrome(CHROME_DRIVE_PATH)
        SHENZHEN_HOURSE_GROUP_LIST_URL = "https://www.douban.com/group/search?cat=1019&q=%E6%B7%B1%E5%9C%B3+%E7%A7%9F%E6%88%BF"
        SAVED_FILE_NAME = "深圳租房Groups.txt"
        crawler = DoubanGroupsCrawler(SHENZHEN_HOURSE_GROUP_LIST_URL, browser, max_pages=MAX_PAGES)
        crawler.start()
        browser.close()
        crawler.save(f"{CRAWLER_FOLDER}/{args.page}", SAVED_FILE_NAME)
    elif args.page == WEB_PAGE.DOUBAN_DISCUSSION_LIST:
        # TODO: move constants to configs.py
        browser = webdriver.Chrome(CHROME_DRIVE_PATH)
        FILTER_DOUBAN_GROUP_LIST_FOLDER = FILTER_FOLDER + "douban_group_list/"
        ALLOWLIST_FILE_NAME = "深圳租房Groups_allowlist.txt"
        MAX_PAGES = sys.maxsize
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
                max_pages=3
            )
            discussions_crawler.start()
        browser.close()
