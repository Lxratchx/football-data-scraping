# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import scrapy.pipelines
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request, Response
from pathlib import PurePosixPath
from urllib.parse import urlparse
import scrapy
from .items import SeasonMapItem


class FootballDataScrapingPipeline(FilesPipeline):
    def file_path(self, request: Request, response: Response=None, info=None, *, item=None):
        *_, season, filename = request.url.split('/')
        return f'{season}/{filename}'


class SeasonMapPipeline:
    def open_spider(self, spider):
        self.file = open("season_maps.json", "w", encoding='utf-8')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.write('{}\n]')
        self.file.close()

    def process_item(self, item, spider):
        if not isinstance(item, SeasonMapItem):
            return item
        
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False, indent=4) + ",\n"
        self.file.write(line)
        return item

