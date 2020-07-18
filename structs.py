#!/usr/bin/python
# -*- coding: UTF-8 -*-

from collections import namedtuple


DoubanGroup = namedtuple("DoubanGroup", ["name", "link", "id", "member_num"])

DoubanDiscussion = namedtuple(
    "DoubanGroup",
    [
        "title",
        "link",
        "discussion_id",
        "group_id",
        "author",
        "num_response",
        "last_update_time",
        "post_time",
        "content",
    ],
)

DoubanDiscussionRent = namedtuple(
    'DoubanDiscussionRent', DoubanDiscussion._fields + ('price',)
)
