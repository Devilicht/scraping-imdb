import scrapy
from pymongo import MongoClient
from imdb250 import settings

class ImdbSpider(scrapy.Spider):
    name = "imdb-scraping-movies"
    start_urls = ["https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"]

    def parse(self, response):
        client = MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        db = client[settings.MONGODV_DB]
        collection = db[settings.MONGODB_COLLECTION]

        for movies in response.css('.titleColumn'):
            item = {
                'titles': movies.css('.titleColumn a ::text').get(),
                'years': movies.css('.secondaryInfo ::text').get(),
                'assessment': response.css('strong ::text').get()
            }
            collection.insert_one(item)
            yield item