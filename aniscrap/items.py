# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SeasonalAnimeItem(scrapy.Item):
    # define the fields for your item here like:
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
