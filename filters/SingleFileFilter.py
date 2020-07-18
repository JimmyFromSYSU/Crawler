#!/usr/bin/python
# -*- coding: UTF-8 -*-

##########################################
# Filter with input of a single file
##########################################

from .Filter import Filter
from pathlib import Path
import json
from structs import DoubanGroup
import sys

class SingleFileFilter(Filter):
    def __init__(self, dir_path: str, file_name: str, limit=sys.maxsize):
        super().__init__(dir_path, limit)
        self.file_name = file_name
        self.allowlist_groups = []

    def process_single_file(self, file_path):
        with open(file_path) as json_file:
            groups = [DoubanGroup._make(group) for group in json.load(json_file)]

        for group in groups:
            name = group.name
            blacklist = [
                # Other districts
                '南山', '宝安', '龙华', '龙岗', '罗湖', '罗宝', '蛇口', '坂田', '光明新区', '西丽', '广州',
                # More
                '同志',
            ]
            if self.filter_by_blocklist(name, blacklist):
                self.allowlist_groups.append(group)

        # Sort by member_num and apply limit
        self.allowlist_groups = sorted(
            self.allowlist_groups,
            key=lambda g: -int(g.member_num)
        )[0: self.limit]

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
