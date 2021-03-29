# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from pymongo import MongoClient
from instagramparser.items import UserFollowerItem


class InstagramparserPipeline:

    # В конструкторе открываем подключение к базе данных
    def __init__(self):
        # Подключаемся к базе и сохраняем подключение в классе
        self.mongodb_client = MongoClient('localhost', 27017)
        self.mongodb_collection = self.mongodb_client['gb_instagram']['users']
        # Очищаем коллекцию от прежних товаров
        self.mongodb_collection.delete_many({})

    # В деструкторе закрываем подключение к базе данных
    def __del__(self):
        self.mongodb_client.close()

    # Обработчик item-ов
    def process_item(self, item: UserFollowerItem, spider):
        # В базе все пользователи храняться в одной коллекции без дублирования.
        # В документе пользователя есть список его подписок (following)
        # Запись в базу пользователя, если его нет
        user = self.read_user_from_db(item['user_name'])
        if user is None:
            # Записываем в базу пользователя, на которого подписан подписчик
            self.mongodb_collection.insert_one(self.prepare_item_for_db(
                item['user_name'], item['user_id'], item['user_full_name'], item['user_photo_url'], None
            ))
        # Запись в базу подписчика или обновление его списка подписок
        follower = self.read_user_from_db(item['follower_name'])
        if follower is None:
            # Записываем в базу подписчика c указанием пользователя в списке подписок
            self.mongodb_collection.insert_one(self.prepare_item_for_db(
                item['follower_name'], item['follower_id'], item['follower_full_name'],
                item['follower_photo_url'], [item['user_name']]
            ))
        else:
            # Обновляем в базе список подписки
            following = follower['following']
            if following is None:
                following = list()
            following.append(item['user_name'])
            self.mongodb_collection.update_one({'name': item['follower_name']}, {'$set': {'following': following}})
        return item

    # Чтение пользователя из базы
    def read_user_from_db(self, user_name):
        return self.mongodb_collection.find_one({'name': user_name})

    # Формирует документ для базы данных
    @staticmethod
    def prepare_item_for_db(user_name, user_id, user_full_name, user_photo_url, user_following):
        return {
            '_id': user_id,
            'name': user_name,
            'full_name': user_full_name,
            'photo_url': user_photo_url,
            'following': user_following
        }
