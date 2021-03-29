# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserFollowerItem(scrapy.Item):
    # Информация о пользователе
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    user_full_name = scrapy.Field()
    user_photo_url = scrapy.Field()
    # Информация о подписчике
    follower_id = scrapy.Field()
    follower_name = scrapy.Field()
    follower_full_name = scrapy.Field()
    follower_photo_url = scrapy.Field()
