# Импортируем класс для создания процесса
from scrapy.crawler import CrawlerProcess

# Импортируем класс для настроек
from scrapy.settings import Settings

# Наши настройки
from instagramparser import settings

# Класс паука
from instagramparser.spiders.instagram import InstagramSpider


if __name__ == '__main__':
    # Создаем объект с настройками
    crawler_settings = Settings()

    # Привязываем к нашим настройкам
    crawler_settings.setmodule(settings)

    # Создаем объект процесса для работы
    process = CrawlerProcess(settings=crawler_settings)

    # Добавляем паука и список пользователей для парсинга
    # users_list = ['name1', 'name2', ...]
    users_list = ['--------', '----']
    process.crawl(InstagramSpider, users_list=users_list)

    # Пуск
    process.start()
