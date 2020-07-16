#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 卓越时代广场：https://ditu.amap.com/dir?from%5Bid%5D=BV10243512-from&from%5Bname%5D=%E7%A6%8F%E7%94%B0%E5%8F%A3%E5%B2%B8(%E5%9C%B0%E9%93%81%E7%AB%99)&from%5Blnglat%5D=114.069273%2C22.515737&from%5Bmodxy%5D=114.069273%2C22.515737&from%5Bpoitype%5D=150500&from%5Badcode%5D=440304&to%5Bname%5D=%E5%8D%93%E8%B6%8A%C2%B7%E6%97%B6%E4%BB%A3%E5%B9%BF%E5%9C%BA&to%5Blnglat%5D=114.057131%2C22.534121&to%5Bid%5D=B02F37T14X-to&to%5Bpoitype%5D=120201&to%5Badcode%5D=440300&to%5Bmodxy%5D=114.057252%2C22.534603&type=bus&policy=0&dateTime=now

from selenium import webdriver
from bs4 import BeautifulSoup
# from MultiPagesCrawler import MultiPagesCrawler
from DoubanGroupsCrawler import DoubanGroupsCrawler
from DoubanGroupDiscussionsCrawler import DoubanGroupDiscussionsCrawler
import json
import os
from filters.Filter import Filter
import re

ALL_DOUBAN_GROUPS_FILE = "douban_groups.txt"
WHITELIST_DOUBAN_GROUPS_FILE = "douban_groups_whitelist.txt"

def save_whitelist_groups():
    with open(ALL_DOUBAN_GROUPS_FILE) as json_file:
        groups = json.load(json_file)
    whitelist_groups = []
    for group in groups:
        name = group['name']
        link = group['link']
        group['id'] = group['link'].strip('/').split('/')[-1]
        blacklist_keyword = [
            '南山', '宝安', '龙华', '龙岗', '罗湖', '广州', '同志', '妹纸',
            '深圳房租太他妈高了党',
            '女人',
            '智租宝，让信息可以共享',
            '深圳豆瓣',
            '深圳拼友',
            '大学',
            '旅游',
            '90后',
            '深圳租房防坑联盟',
            '拉拉',
            '深圳信息衣食住行吃喝玩乐',
            '深圳视窗',
        ]

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


def test_filter():
    path = os.getcwd() + "/data/discussions/"
    filter_ = Filter(path)
    filter_.start()


def print_discussion(file_path):
    with open(file_path) as json_file:
        discussion = json.load(json_file)
    print(discussion)


# save_all_groups()

save_whitelist_groups()
print_whitelist_groups()

# test_single_discussion_page()
# print_discussion("/Users/zhiliu/Desktop/script/crawler/data/discussions/106955/169763419")

# test_filter()
# save_all_discussions()
