#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
# from MultiPagesCrawler import MultiPagesCrawler
from DoubanGroupsCrawler import DoubanGroupsCrawler
from DoubanGroupDiscussionsCrawler import DoubanGroupDiscussionsCrawler
import json
import os
from filters.Filter import Filter
import re

CHROME_DRIVE_PATH = "./bin/chromedriver"
SHENZHEN_HOURSE_GROUP_LIST_URL = "https://www.douban.com/group/search?cat=1019&q=%E6%B7%B1%E5%9C%B3+%E7%A7%9F%E6%88%BF"

ALL_DOUBAN_GROUPS_FILE = "douban_groups.txt"
WHITELIST_DOUBAN_GROUPS_FILE = "douban_groups_whitelist.txt"


def save_all_groups():
    browser = webdriver.Chrome(CHROME_DRIVE_PATH)
    groups_crawler = DoubanGroupsCrawler(SHENZHEN_HOURSE_GROUP_LIST_URL, browser)
    groups_crawler.start()
    browser.close()
    groups = groups_crawler.get_groups()
    with open(ALL_DOUBAN_GROUPS_FILE, 'w') as outfile:
        json.dump(groups, outfile)


def save_whitelist_groups():
    with open(ALL_DOUBAN_GROUPS_FILE) as json_file:
        groups = json.load(json_file)
    whitelist_groups = []
    for group in groups:
        name = group['name']
        link = group['link']
        group['id'] = group['link'].strip('/').split('/')[-1]
        blacklist_keyword = ['南山', '宝安', '龙华', '龙岗', '罗湖', '广州']

        is_good = True
        for keyword in blacklist_keyword:
            if name.find(keyword) >= 0:
                is_good = False
                break
        if is_good:
            whitelist_groups.append(group)

    with open(WHITELIST_DOUBAN_GROUPS_FILE, 'w') as outfile:
        json.dump(whitelist_groups, outfile)


def print_whitelist_groups():
    with open(WHITELIST_DOUBAN_GROUPS_FILE) as json_file:
        groups = json.load(json_file)

    print(f"total count: {len(groups)}")
    for group in groups:
        name = group['name']
        link = group['link']
        gid = group['id']
        print(f"{name} [{gid}]: {link}")


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


def test_filter():
    path = os.getcwd() + "/data/discussions/"
    filter_ = Filter(path)
    filter_.start()


def print_discussion(file_path):
    with open(file_path) as json_file:
        discussion = json.load(json_file)
    print(discussion)


save_all_discussions()
# test_single_discussion_page()
