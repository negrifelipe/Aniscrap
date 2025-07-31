# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AnimeItem(scrapy.Item):
    id:int = scrapy.Field()
    picture_url: str = scrapy.Field()
    names: {
        'english': str,
        'japanese': str
    } = scrapy.Field()
    synopsis:str = scrapy.Field()
    statics: {
        'score': float,
        'rank': int,
        'popularity': int,
        'members': int,
        'favorites': int
    } = scrapy.Field()
    anime_type: {'name': str, 'url': str } = scrapy.Field()
    episodes: int = scrapy.Field()
    status: str = scrapy.Field()
    aired: str = scrapy.Field()
    premiered: str = scrapy.Field()
    broadcast: str = scrapy.Field()
    producers: [{'name': str, 'url': str }] = scrapy.Field()
    licensors: [{'name': str, 'url': str }] = scrapy.Field()
    studios: [{'name': str, 'url': str }]  = scrapy.Field()
    source: {'name': str, 'url': str } = scrapy.Field()
    genres: [{'name': str, 'url': str }] = scrapy.Field()

class SearchAnimeResultItem(scrapy.Item):
    id: int = scrapy.Field()
    picture_url: str = scrapy.Field()
    name: str = scrapy.Field()
    url: str = scrapy.Field()
    synopsis: str = scrapy.Field()
    anime_type: str = scrapy.Field()
    episodes: int = scrapy.Field()
    score: float = scrapy.Field()

class SeasonalAnimeItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    picture_url = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    anime_type = scrapy.Field()
    synopsis = scrapy.Field()
    studios = scrapy.Field()
    source = scrapy.Field()
    themes = scrapy.Field()
    demographic = scrapy.Field()
    aired = scrapy.Field()
    
    pass
