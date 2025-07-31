from urllib.parse import quote

import scrapy
from scrapy.http import Request, Response
from aniscrap.items import SearchAnimeResultItem

class SearchAnimeSpider(scrapy.Spider):
    name = "search-anime"
    allowed_domains = ["myanimelist.net"]

    def __init__(self, name: str | None = None, *args, **kwargs):
        if name is None:
            raise ValueError('Anime name is required. Example "scrapy crawl search-anime -a name=kaoru"')
        self.name = name

    async def start(self):
        yield Request(f'https://myanimelist.net/anime.php?cat=anime&q={quote(self.name)}')

    def parse(self, response: Response):
        animes = response.css('div.js-categories-seasonal > table > tr')
       
        for anime in animes[1:]:
            item = SearchAnimeResultItem()
            item['picture_url'] = anime.css('td > div > a > img::attr(data-src)').get()
            item['name'] = anime.css('div.title > a > strong::text').get()
            item['url'] = anime.css('a::attr(href)').get()
            item['id'] = int(item['url'].split('/')[4])
            item['synopsis'] = anime.css('div.pt4::text').get()
            item['anime_type'] = anime.css('td:nth-child(3)::text').get().strip()
            episodes = anime.css('td:nth-child(4)::text').get().strip()
            item['episodes'] = int(episodes) if episodes != '-' else 0
            score = anime.css('td:nth-child(5)::text').get().strip()
            item['score'] = float(score) if score != 'N/A' else 0
            yield item

        pass
