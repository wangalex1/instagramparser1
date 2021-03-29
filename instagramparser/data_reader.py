 

from pymongo import MongoClient


def get_followers_count(user_name, db_coll):
    """Функция возвращает количество подписчиков указанного пользователя."""
    return db_coll.count_documents({'following': {'$in': [user_name]}})


def print_followers(user_name, db_coll):
    """Функция печатает всех подписчиков указанного пользователя"""
    followers = db_coll.find({'following': {'$in': [user_name]}})
    if followers:
        print(f'Подписчики пользователя {user_name}:')
        for ind, follower in enumerate(followers, 1):
            if follower["full_name"]:
                print(f'{ind}) {follower["full_name"]} (@{follower["name"]})')
            else:
                print(f'{ind}) {follower["name"]}')


def print_following(user_name, following_list, db_coll):
    """Функция печатает все подписки указанного пользователя"""
    following = db_coll.find({'name': {'$in': following_list}})
    if following:
        print(f'Подписки пользователя {user_name}:')
        for ind, follow in enumerate(following, 1):
            if follow["full_name"]:
                print(f'{ind}) {follow["full_name"]} (@{follow["name"]})')
            else:
                print(f'{ind}) {follow["name"]}')


print('Программа для работы с базой Instagram')
username = input('Введите имя пользователя Instagram: ')

# Открываем подключение к базе данных
mongodb_client = MongoClient('localhost', 27017)
mongodb_collection = mongodb_client['gb_instagram']['users']

# Поиск пользователя и печать общей информации
user = mongodb_collection.find_one({'name': username})
if user:
    print('Есть информация об этом пользователе в нашей базе данных!')
    print(f'Логин: {user["name"]}. Полное имя: {user["full_name"]}')
    print('Количество подписчиков:', get_followers_count(username, mongodb_collection))
    print('Количество подписок:', len(user["following"]))
    print('Список команд:')
    print(' 1 - напечатать всех подписчиков')
    print(' 2 - напечатать все подписки')
    print(' 3 - напечатать оба списка')
    print(' 0 - выход')
    command = input('Введите команду: ')
    if command == '1':
        print_followers(username, mongodb_collection)
    elif command == '2':
        print_following(username, user['following'], mongodb_collection)
    elif command == '3':
        print_followers(username, mongodb_collection)
        print('-' * 50)
        print_following(username, user['following'], mongodb_collection)
else:
    print('Такого пользователя в нашей базе данных нет.')

# Закрываем подключение к базе данных
mongodb_client.close()
