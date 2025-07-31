import locale
import scrapy
from scrapy.http import Request, Response
from scrapy.selector import SelectorList
from aniscrap.items import AnimeItem

class AnimeSpider(scrapy.Spider):
    """Spider for scraping anime by id from MyAnimeList.
    
    This spider parses all anime information from the anime page.
    However it does not include characters, staff and reviews.
    """
    name = "anime"
    
    def __init__(self, id: int | None = None, *args, **kwargs):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
        if id is None:
            raise ValueError('Anime ID is required. Example "scrapy crawl anime -a id=59845"')
        self.id = id
        

    async def start(self):
        yield Request(f"https://myanimelist.net/anime/{self.id}")

    def parse(self, response: Response):
        item = AnimeItem()
        item['id'] = self.id
        item['picture_url'] = response.css('.leftside .lazyload').attrib['data-src']
        item['names'] = self.parse_names(response)
        item['synopsis'] = '\n'.join(text.strip() for text in response.xpath('//p[contains(@itemprop, "description")]//text()').getall())
        item['statics'] = self.parse_statics(response)
        item['anime_type'] =self.parse_name_and_url_from_left_side(response, 'Type:')
        item['episodes'] = int(self.parse_text_from_left_side(response, 'Episodes:'))
        item['status'] = self.parse_text_from_left_side(response, 'Status:')
        item['broadcast'] = self.parse_text_from_left_side(response, 'Broadcast:')
        item['aired'] = self.parse_text_from_left_side(response, 'Aired:')
        item['premiered'] = self.parse_text_from_left_side(response, 'Premiered:')
        item['producers'] = self.parse_names_and_urls_from_left_side(response, 'Producers:')
        item['licensors'] = self.parse_names_and_urls_from_left_side(response, 'Licensors:')
        item['studios'] = self.parse_names_and_urls_from_left_side(response, 'Studios:')
        item['source'] = self.parse_name_and_url_from_left_side(response, 'Source:')
        item['genres'] = self.parse_names_and_urls_from_left_side(response, 'Genres:')

        return item

    def parse_names(self, response: Response):
        names = {}

        names['english'] = response.css('h1.title-name > strong::text').get()
        names['japanese'] = self.parse_text_from_left_side(response, 'Japanese:')

        return names

    def parse_statics(self, response: Response):
        return {
            'score': float(self.get_from_left_side(response, 'Score:').xpath('.//span[@itemprop="ratingValue"]//text()').get()), 
            'rank': int(self.get_from_left_side(response, 'Ranked:').xpath('.//text()').getall()[2].strip().removeprefix('#')),
            'popularity': int(self.get_from_left_side(response, 'Popularity:').xpath('.//text()').getall()[2].strip().removeprefix('#')),
            'members': locale.atoi(self.parse_text_from_left_side(response, 'Members:')),
            'favorites': locale.atoi(self.parse_text_from_left_side(response, 'Favorites:'))
        }

    def parse_name_and_url_from_left_side(self, response: Response, key: str):
        element = self.get_from_left_side(response, key)
        return {
            'name': element.xpath('.//a//text()').get().strip(),
            'url': element.xpath('.//a//@href').get()
        }

    def parse_names_and_urls_from_left_side(self, response: Response, key: str):
        elements = self.get_from_left_side(response, key).xpath('.//a')
        return [
            {
                'name': element.xpath('.//text()').get().strip(),
                'url': element.xpath('.//@href').get()
            }
            for element in elements
        ]

    def parse_text_from_left_side(self, response: Response, key:str) -> str:
        texts = self.get_from_left_side(response, key).xpath('.//text()[not(parent::span)]').getall()
        return ' '.join(text.strip() for text in texts if text.strip())

    def get_from_left_side(self, response: Response, key: str) -> SelectorList:
        return response.xpath(f'//div[contains(@class, "spaceit_pad") and .//span[text()="{key}"]]')