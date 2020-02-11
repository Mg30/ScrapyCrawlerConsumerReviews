# ScrapyCrawlerConsumerReviews
Création d'un crawler scrapy permettant l’acquisition de données d'avis de consommateurs issus d'un site web

## Installation

### python dependencies 
`pip install -r requirements.txt`

### docker splash 
`docker pull scrapinghub/splash`



## Lancement

`docker run -p 8050:8050  scrapinghub/splash`
`cd avisconso`
`scrapy crawl brandavis -o <filename>.json`
