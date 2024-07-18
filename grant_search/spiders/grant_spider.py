import scrapy
from grant_urls import grant_urls

class GrantsSpider(scrapy.Spider):
    name = 'grants'
    start_urls = grant_urls

    def parse(self, response):
        for grant in response.css('div.grant-item'):
            yield {
                'title': grant.css('h2::text').get(),
                'amount': grant.css('span.amount::text').get(),
                'deadline': grant.css('span.deadline::text').get(),
                'url': grant.css('a::attr(href)').get(),
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
