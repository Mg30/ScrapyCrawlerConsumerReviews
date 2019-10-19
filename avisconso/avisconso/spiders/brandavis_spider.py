import scrapy
from scrapy_splash import SplashRequest
from scrapy.utils.response import open_in_browser
from scrapy.http import HtmlResponse


class BrandAvisSpider(scrapy.Spider):
    name = "brandavis"
    start_urls = [
        "https://monavislerendgratuit.com/avis/gazeuses-aromatisees/eaux/san-pellegrino/san-pellegrino-limone-tea-ou-pesca-tea"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, self.parse, endpoint="render.html", args={"wait": 0.5}
            )

    def parse(self, response):
        pages = []
        for number_pages in response.xpath('//ul[@class="pags clearfix"]/li[@class="limit"]/a/@rel').getall():
            pages.append(int(number_pages))

        if len(pages) > 0:
            max_page = max(pages)
            current_page = 0

            while current_page < max_page:
                current_page += 1
                url_current_page = response.url + f'/{str(current_page)}'
                yield SplashRequest(
                    url_current_page,
                    self.parse_review,
                    endpoint="render.html",
                    args={"wait": 5},
                )

    def parse_review(self, response):

        product_name = response.xpath('//h1[@itemprop="name"]/text()').get()
        product_rating = response.xpath(
            '//div[@class="product-rating"]//input/@value'
        ).get()

        for review in response.xpath(
            '//li[@class="clearfix review-item margin-top10 e-review-item row   "]'
        ).getall():
            review_html = HtmlResponse(
                url="reponse", body=str(review), encoding="utf-8"
            )
            comment = review_html.xpath(
                '//p[@class="review-body"]/text()').get()
            rated = review_html.xpath(
                '//input[@name="rating-loading"]/@value').get()
            date = review_html.xpath(
                '//p[@class="date align-right"]/text()').get()
            user_space_url = review_html.xpath(
                '//a[@title="Visitez son espace personnel"]/@href').get()
            yield SplashRequest(
                user_space_url,
                self.parse_user,
                endpoint="render.html",
                args={"wait": 5},
                meta={'item': {
                    "product_name": product_name,
                    "product_avg_rate": product_rating,
                    "comment": comment,
                    "consummer_rate": rated,
                    "date": date}
                }
            )

    def parse_user(self, response):
        username = response.xpath(
            '//div[@class="user-info"]//span[@class="T4blue"]/text()').get()
        user_info = response.xpath(
            '//div[@class="user-info"]//span[@class="T5darkgray"]/text()').getall()
        parse_result = response.meta['item']
        parse_result['username'] = username
        parse_result['user_info'] = user_info
        yield parse_result
