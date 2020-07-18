# Crawler
## Example

(1) Crawl all related douban groups
```
python3 crawler.py --type douban_group_list
```

(2) Filter the douban groups and limit the number of groups to crawl
```
python3 filter.py --type douban_group_list --limit 3
```

(3) Crawl all discussions in the first page of the groups in the allowlist
```
python3 crawler.py --type douban_discussion_list --limit 1
```

(4) Filter discussion by hard coded rules
```
python3 filter.py --type douban_discussion_list
```

## TODO
* For now, all filter rules are hard coded. Next step is to make it configerable.
