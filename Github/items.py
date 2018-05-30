# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GithubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    repositories = scrapy.Field()
    stars = scrapy.Field()
    followers = scrapy.Field()
    followings = scrapy.Field()


class GithubRepoItem(scrapy.Item):
    repo = scrapy.Field()
    fork = scrapy.Field()
    star = scrapy.Field()
    language = scrapy.Field()
