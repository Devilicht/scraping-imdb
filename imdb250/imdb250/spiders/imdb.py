import scrapy


class ImdbSpider(scrapy.Spider):
    name = "imdb-scraping-movies"
    start_urls = ["https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"]

    def parse(self, response):
        for movies in response.css('.titleColumn'):
            yield{
            'titles' : movies.css('.titleColumn a ::text').get(),
            'years' : movies.css('.secondaryInfo ::text').get(),
            'assessment' : response.css('strong ::text').get()
              }
