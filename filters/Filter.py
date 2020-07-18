#!/usr/bin/python
# -*- coding: UTF-8 -*-
from os import listdir
from os.path import isfile, join
import re
import json
from typing import Optional
import sys
# discussions = {
#     'title':
#     'link':
#     'discussion_id':
#     'group_id':
#     'author':
#     'num_response':
#     'last_update_time':
#     'post_time':
#     'content':
# }


class Filter:
    def __init__(self, dir_path: str, limit=sys.maxsize):
        self.dir_path = dir_path.rstrip('/') + '/'
        self.limit = limit
        # print(self.dir_path)
        self.discussions = []
        self.authors = set()

    def filter_by_blocklist(self, text:str, blocklist) -> bool:
        for keyword in blocklist:
            if text.find(keyword) >= 0:
                return False
        return True

    def TEXT_CONTAIN(self, key_word: str, discussion) -> bool:
        content = discussion['content']
        title = discussion['title']
        return (
            re.search(key_word, title, re.IGNORECASE) or
            re.search(key_word, content, re.IGNORECASE)
        )

    def merge_condition(self, MUST_TRUE, MUST_FALSE) -> bool:
        # print(MUST_TRUE)
        for item in MUST_TRUE:
            if item:
                continue
            else:
                return False

        # print(MUST_FALSE)
        for item in MUST_FALSE:
            if item:
                return False

        return True

    def extract_price(self, text: str) -> Optional[int]:
        def normalize(price_str: str) -> int:
            if price_str[-1] == 'k':
                price = int(price_str[0:-1]) * 1000
            else:
                price = int(price_str)
            return price

        pattern = re.compile("(价格低至|仅租|价格|月租|租金|房租|一人)(是?)(\d+k?)", re.IGNORECASE)
        m = pattern.search(text)
        if m and len(m.groups()) == 3:
            return normalize(m.group(3))

        pattern = re.compile("(\d+)(元*)(/|每|一个)月", re.IGNORECASE)
        m = pattern.search(text)
        if m and len(m.groups()) == 3:
            return int(m.group(1))

        pattern = re.compile("(\d{4})(元|月)", re.IGNORECASE)
        m = pattern.search(text)
        if m and len(m.groups()) == 2:
            return int(m.group(1))

        pattern = re.compile("实价(\d+)", re.IGNORECASE)
        m = pattern.search(text)
        if m and len(m.groups()) == 1:
            return int(m.group(1))

        return None

    def extract_title_price(self, text: str) -> Optional[int]:
        price = self.extract_price(text)
        if price is None:
            pattern = re.compile("(\d{4})", re.IGNORECASE)
            m = pattern.search(text)
            if m and len(m.groups()) == 1:
                return int(m.group(1))
        return price

    def filter(self, discussion) -> bool:
        post_time = discussion['post_time']
        if post_time[0:10] < '2020-06-01':
            return False

        location = "福田"
        # 地铁口：https://www.amap.com/dir?from%5Bid%5D=BV10249966&from%5Bname%5D=%E8%8E%B2%E8%8A%B1%E6%9D%91(%E5%9C%B0%E9%93%81%E7%AB%99)&from%5Blnglat%5D=114.067829%2C22.548646&from%5Bmodxy%5D=114.067829%2C22.548646&from%5Bpoitype%5D=150500&from%5Badcode%5D=440304&to%5Bname%5D=%E5%8D%93%E8%B6%8A%C2%B7%E6%97%B6%E4%BB%A3%E5%B9%BF%E5%9C%BA&to%5Blnglat%5D=114.057131%2C22.534121&to%5Bid%5D=B02F37T14X-to&to%5Bpoitype%5D=120201&to%5Badcode%5D=440300&to%5Bmodxy%5D=114.057252%2C22.534603&type=car&policy=1
        # 石厦：6mins
        # 岗厦: 7mins
        # 沙尾：7mins
        # 景田：9mins
        # 赤尾：9mins
        # 香梅：10mins
        # 莲花村：11mins
        # 上梅林：13mins
        # 华侨城：14mins
        # 八卦岭：15mins
        # 桃源村：16mins
        MUST_TRUE = [
            self.TEXT_CONTAIN("福田", discussion),
            # self.TEXT_CONTAIN("(舍友|室友|合租)", discussion),
            # self.TEXT_CONTAIN("loft", discussion),
            self.TEXT_CONTAIN(r"[2|两｜二｜][房|室|居]", discussion),
        ]

        MUST_FALSE = [
            # self.TEXT_CONTAIN(r"[2|3|4|5|两｜二｜三|四|五][房|室|居]", discussion),
            self.TEXT_CONTAIN(r"[3|4|5｜三|四|五][房|室|居]", discussion),
            self.TEXT_CONTAIN(r"已出租", discussion),
            # self.TEXT_CONTAIN(r"求租", discussion),
            self.TEXT_CONTAIN(r"求(整?)租", discussion),
            self.TEXT_CONTAIN(r"求房源", discussion),
            # self.TEXT_CONTAIN("(舍友|室友|合租)", discussion),
        ]

        return self.merge_condition(MUST_TRUE, MUST_FALSE)

    # TODO: all filter rules are hard coded for now, make this configerable.
    def process_single_file(self, file_path):
        with open(file_path) as json_file:
            discussion = json.load(json_file)
        if self.filter(discussion):
            title = discussion['title']
            content = discussion['content']
            author = discussion['author']
            # link = discussion['link']
            price = self.extract_price(content)
            if price is None:
                price = self.extract_title_price(title)

            if price is None or (price >= 3000 or price <= 500):
                if author not in self.authors:
                    discussion['price'] = price
                    self.discussions.append(discussion)
                    self.authors.add(author)


    def print_discussions(self):
        self.discussions = sorted(self.discussions, key=lambda discussion: discussion['post_time'])
        # self.discussions = sorted(self.discussions, key=lambda discussion: discussion['last_update_time'])
        count = 0
        for discussion in self.discussions:
            author = discussion['author']
            title = discussion['title']
            content = discussion['content']
            link = discussion['link']
            post_time = discussion['post_time']
            last_update_time = discussion['last_update_time']
            price = discussion['price']
            count = count + 1
            # print(f"{str(count).zfill(4)} {post_time} 价格: {price}元/月 {title}: {link}")
            print(f"{post_time[0:10]} 价格: {price}元/月 ({author}) \t {title}: {link}\n")
            # print(f"{str(count).zfill(4)} {last_update_time} 价格: {price}元/月 {title}: {link}")


    def traverse_all_files(self, process):
        self.discussions = []
        group_dirs = listdir(self.dir_path)

        for group_dir in group_dirs:
            if group_dir == '.DS_Store':
                continue
            group_path = self.dir_path + group_dir + "/"
            discussion_files = listdir(group_path)
            for discussion_file in discussion_files:
                discussion_file_path = group_path + discussion_file
                process(discussion_file_path)

        self.print_discussions()

    def start(self):
        self.traverse_all_files(self.process_single_file)
