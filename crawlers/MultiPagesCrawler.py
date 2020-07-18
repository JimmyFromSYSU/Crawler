#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Optional
from selenium import webdriver
from bs4 import BeautifulSoup
import logging
import sys
from constants import LOGGER_FORMAT

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)

class MultiPagesCrawler:
    def __init__(self, url: str, browser, max_pages: int=sys.maxsize):
        self.url = url
        self.browser = browser
        self.max_pages = max_pages

    def content(self, a):
        return " ".join(a.contents)

    def fetch(self, url: str):
        logger.info(f"fetching {url}")
        self.browser.get(url)
        page = {
            'title': self.browser.title,
            'page_source': self.browser.page_source,
        }
        return page

    def last_section(self, url) -> str:
        return url.strip('/').split('/')[-1]

    def next_url(self, soup) -> Optional[str]:
        return None

    def process_page(self, soup) -> bool:
        return True

    def start(self):
        cur_url = self.url
        page_count = 0
        while(cur_url and page_count < self.max_pages):
            logger.info(f"page #{page_count}")
            page = self.fetch(cur_url)
            soup = BeautifulSoup(page['page_source'], "html.parser")
            continue_ = self.process_page(soup)
            if continue_ is False:
                break
            page_count = page_count + 1
            cur_url = self.next_url(soup)
