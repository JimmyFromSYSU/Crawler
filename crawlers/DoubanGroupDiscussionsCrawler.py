#!/usr/bin/python
# -*- coding: UTF-8 -*-
from typing import Optional
from bs4 import BeautifulSoup
from .MultiPagesCrawler import MultiPagesCrawler
import re
from os import path
from pathlib import Path
import json
import sys
import logging
from structs import DoubanDiscussion
from constants import CRAWLER_FOLDER, CRAWLER_TYPE, LOGGER_FORMAT
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT)


class DoubanGroupDiscussionsCrawler(MultiPagesCrawler):
    def __init__(self, url: str, group_id: str, browser, max_pages: int=sys.maxsize):
        super().__init__(url, browser, max_pages)
        self.discussions = []
        self.group_id = group_id

    def rows_to_discussions(self, trs):
        trs = [tr for tr in trs if 'th' not in tr.attrs['class']]
        for tr in trs:
            tds = tr.find_all('td')
            title_link = tds[0].find('a')
            author_link = tds[1].find('a')
            self.discussions.append(DoubanDiscussion(
                title=self.content(title_link).strip(),
                link=title_link['href'],
                discussion_id=self.last_section(title_link['href']),
                group_id=self.group_id,
                author=self.content(author_link),
                num_response=self.content(tds[2]),
                last_update_time=self.content(tds[3]),
                post_time=None,
                content=None
            ))

    def next_url(self, soup) -> Optional[str]:
        next_span = soup.body.find("span", class_="next")
        if next_span:
            next_link = next_span.find("a")
            if next_link:
                return next_link['href']
        return None

    def fetch_discussion_page(self, discussion):
        url = discussion.link
        page = self.fetch(url)
        soup = BeautifulSoup(page['page_source'], "html.parser")
        return soup

    def get_discussion_file_path(self, discussion):
        dir_ = self.get_discussion_file_dir(discussion)
        discussion_id = discussion.discussion_id
        return f"{dir_}/{discussion_id}"

    def get_discussion_file_dir(self, discussion):
        group_id = discussion.group_id
        return f"{CRAWLER_FOLDER}/{CRAWLER_TYPE.DOUBAN_DISCUSSION_LIST}/{group_id}"

    def process_discussion_page(self, soup, discussion):
        post_time_span = soup.find(class_="topic-doc").find("span", class_="color-green")
        discussion = discussion._replace(
            post_time=self.content(post_time_span),
            content=soup.find(class_="topic-content").get_text()
        )
        Path(self.get_discussion_file_dir(discussion)).mkdir(parents=True, exist_ok=True)
        with open(self.get_discussion_file_path(discussion), 'w+') as outfile:
            json.dump(discussion, outfile)

    def process_page(self, soup) -> bool:
        content = soup.find(id="content")
        rows = content.find_all('tr')
        objs = self.rows_to_discussions(rows)
        for discussion in self.discussions:
            file_path_str = self.get_discussion_file_path(discussion)
            p = Path(file_path_str)
            if p.exists():
                logger.info(f"ignore {file_path_str}")
                continue
            soup = self.fetch_discussion_page(discussion)
            self.process_discussion_page(soup, discussion)
        return True

    def get_discussions(self):
        return self.discussions
