#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Optional
from bs4 import BeautifulSoup
from MultiPagesCrawler import MultiPagesCrawler

class DoubanGroupsCrawler(MultiPagesCrawler):
    def __init__(self, url: str, browser):
        super().__init__(url, browser)
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
            self.groups.append({
                'name': " ".join(link.contents),
                'link': link['href'],
                'id': self.last_section(link['href'])
            })
        return True


    def get_groups(self):
        return self.groups
