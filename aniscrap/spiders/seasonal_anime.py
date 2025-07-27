import scrapy

from aniscrap.items import SeasonalAnimeItem

class SeasonalAnimeSpider(scrapy.Spider):
    """Spider for scraping seasonal anime from MyAnimeList.
    
    This spider parses anime information from the current season animes,
    including name, URL, picture, type, synopsis, studios, source, themes and demographic.
    """
    name = "seasonal-anime"
    allowed_domains = ["myanimelist.net"]
    start_urls = ["https://myanimelist.net/anime/season"]

    def parse(self, response):
        categories = response.css('div.js-seasonal-anime-list')

        for category in categories:
            anime_type = category.css('div.anime-header::text').get()
            
            # Get all anime entries in this category
            animes = category.css('div.seasonal-anime')

            for anime in animes:
                yield self.parse_anime(anime, anime_type)
    
    def parse_anime(self, anime, anime_type):
        item = SeasonalAnimeItem()
        item['name'] = anime.css('h2.h2_anime_title > a::text').get()
        item['url'] = anime.css('h2.h2_anime_title > a::attr(href)').get()
        item['picture_url'] = anime.css('img::attr(src)').get() or anime.css('img::attr(data-src)').get()
        item['anime_type'] = anime_type
        item['synopsis'] = anime.css('p.preline::text').get()

        # Parse additional properties (studios, source, themes and demographic)
        properties = anime.css('div.synopsis > div.properties > div')
        for property in properties:
            property_name = property.css('span.caption::text').get()
            property_values = property.css('span.item')
            
            if property_name == 'Studio' or property_name == 'Studios':
                item['studios'] = self.parse_property_link_list(property_values)
            elif property_name == 'Source':
                item['source'] = self.parse_property_value(property_values)
            elif property_name == 'Theme' or property_name == 'Themes':
                item['themes'] = self.parse_property_link_list(property_values)
            elif property_name == 'Demographic':
                item['demographic'] = self.parse_property_value(property_values)
        return item
    
    def parse_property_link_list(self, property_values):
        values = []
        
        for property in property_values:
            relative_url = property.xpath('.//a/@href').get()
            
            if relative_url is None:
                continue
                
            values.append({
                'name': property.xpath('.//a//text()').get(),
                'url': f"https://myanimelist.net{relative_url}"
            })
            
        return values

    def parse_property_value(self, property_values):
        return property_values.xpath('.//text()').get()
