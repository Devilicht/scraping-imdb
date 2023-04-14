from bs4 import BeautifulSoup
from requests import get
from pymongo import MongoClient

client = MongoClient('mongodb://root:3030@mongo:27017/')

db = client.plataformMoviesRank
collection = db.imdbMoviesRank

userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
headers = {'User-Agent': userAgent}

url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"

response = get(url,headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

ranks = soup.select('.ratingColumn.imdbRating')
titlesMovies = soup.select('.titleColumn')

movies = [{'id': i + 1,
'name': title.select_one('a').get_text(strip=True),
'years': title.select_one('span').get_text(strip=True),
'rank': ranks[i].select_one('strong').get_text(strip=True)}
for i, title in enumerate(titlesMovies)]

collection.insert_many(movies)

client.close()
