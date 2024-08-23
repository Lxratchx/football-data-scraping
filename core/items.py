# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FootballDataScrapingItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


class SeasonMapItem(scrapy.Item):
    abbreviation = scrapy.Field()
    value = scrapy.Field()
