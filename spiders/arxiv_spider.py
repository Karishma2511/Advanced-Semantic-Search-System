import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class ArxivSpider(CrawlSpider):
    name = 'arxiv'
    allowed_domains = ['arxiv.org']
    start_urls = ['https://arxiv.org/list/cs/new']
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 8
    }

    rules = (
        Rule(LinkExtractor(allow=('/abs/', '/pdf/')), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # Use BeautifulSoup to parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract_text = soup.select_one('blockquote.abstract').get_text(strip=True) if soup.select_one('blockquote.abstract') else 'No abstract found'

        yield {
            'title': response.xpath('//h1[contains(@class,"title")]/text()').get().strip(),
            'url': response.url,
            'abstract': abstract_text,
        }
