import scrapy
from ..items import SeasonMapItem


class SeasonMapSpider(scrapy.Spider):
    name = 'football-data-season-map'
    allowed_domains = ['football-data.co.uk']
    start_urls = [

    ]
    