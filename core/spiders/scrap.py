import re
from scrapy.http import Request, Response

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import SeasonMapItem

# https://www.football-data.co.uk/mmz4281/2425/E0.csv

class FootballDataScrapingSpider(CrawlSpider):
    name = 'football-data'
    allowed_domains = ['football-data.co.uk']
    start_urls = ['https://www.football-data.co.uk/data.php']
    
    rules = (
        Rule(
            LinkExtractor(
                allow=(r'[a-z]+m\.php$',),
                deny=('downloadm.php', 'profitable_betting_system.php', '/blog/')
            ),
            callback='map_seasons',
            follow=True
        ),
        Rule(LinkExtractor(allow=(r'mmz4281/\d{4}/\w+\.csv$',)), callback='parse_item'),
    )
    
    def __process_abbrevation(self, abb):
        find_results = re.findall(r'\w+\.csv', abb)
        if not find_results:
            return abb
        
        result = find_results[0].split('.')[0]
        return result

    def map_seasons(self, response):
        abbreviations = response.xpath('//a[contains(@href, ".csv")]/@href').getall()
        abbreviations = list(map(self.__process_abbrevation, abbreviations))

        values = response.xpath('//a[contains(@href, ".csv")]/text()').getall()
        items = (SeasonMapItem(abbreviation=abb, value=val) for abb, val in zip(abbreviations, values))
        yield from items

    def parse_item(self, response: Response):
        yield {
            'file_urls': [response.url]
        }
