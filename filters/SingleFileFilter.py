#!/usr/bin/python
# -*- coding: UTF-8 -*-

##########################################
# Filter with input of a single file
##########################################

from .Filter import Filter
from pathlib import Path
import json
from structs import DoubanGroup

class SingleFileFilter(Filter):
    def __init__(self, dir_path: str, file_name: str):
        super().__init__(dir_path)
        self.file_name = file_name
        self.allowlist_groups = []

    def process_single_file(self, file_path):
        with open(file_path) as json_file:
            groups = [DoubanGroup._make(group) for group in json.load(json_file)]

        whitelist_groups = []
        for group in groups:
            name = group.name
            blacklist = [
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
            if self.filter_by_blocklist(name, blacklist):
                self.allowlist_groups.append(group)

        self.print()

    def print(self):
        groups = self.allowlist_groups
        print(f"total count: {len(groups)}")
        count = 0
        for group in groups:
            print(f"{count}: ({group.member_num} members) {group.name}: {group.link}")
            count = count + 1

    def save(self, dir_path: str, file_name: str) -> None:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        with open(f"{dir_path}/{file_name}", 'w') as outfile:
            json.dump(self.allowlist_groups, outfile)

    def start(self):
        self.process_single_file(self.dir_path + self.file_name)
