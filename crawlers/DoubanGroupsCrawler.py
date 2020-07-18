#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Optional
from bs4 import BeautifulSoup
from .MultiPagesCrawler import MultiPagesCrawler
from structs import DoubanGroup
import json
from pathlib import Path
import sys

class DoubanGroupsCrawler(MultiPagesCrawler):
    def __init__(self, url: str, browser, max_pages: int=sys.maxsize):
        super().__init__(url, browser, max_pages)
        self.groups = []

    def next_url(self, soup) -> Optional[str]:
        next_span = soup.body.find("span", class_="next")
        if next_span:
            next_link = next_span.find("a")
            if next_link:
                return next_link['href']
        return None

    def process_page(self, soup) -> bool:
        result_divs = soup.body.find_all("div", class_="result")
        content_divs = [result_div.find("div", class_="content") for result_div in result_divs]
        groups = []
        for content_div in content_divs:
            link = content_div.find('a')
            info = content_div.find(class_='info')
            self.groups.append(
                DoubanGroup(
                    name=" ".join(link.contents),
                    link=link['href'],
                    id=self.last_section(link['href']),
                    # Example: <div class="info">264397 个深圳租房-南山租房 在此聚集 </div>
                    member_num=self.content(info).split(" ")[0],
                )
            )
        return True

    def save(self, dir_path, file_name) -> bool:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        with open(f"{dir_path}/{file_name}", 'w') as outfile:
            json.dump(self.groups, outfile)
        return True

    def get_groups(self):
        return self.groups
