import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CitilinkSearchSpider(CrawlSpider):
    name = 'citilink_search'
    allowed_domains = ['www.citilink.ru']
    start_urls = ['https://www.citilink.ru/search/?text=Gaming+notebook']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='ProductCardVertical__description ']/a",
                           process_value=lambda link: link + 'properties'),
             callback='parse_item',
             follow=True),
    )

    def parse_item(self, response):
        spec_dict = {}
        specs = response.xpath("//div[@class='Specifications__row']")
        for spec in specs:
            key = spec.xpath(
                ".//div[@class='Specifications__column Specifications__column_name']/text()").get().strip()
            spec_dict[key] = spec.xpath(
                ".//div[@class='Specifications__column Specifications__column_value']/text()").get().strip()

        yield {
            'title': response.xpath("normalize-space(//h1/text())").get(),
            'rating': response.xpath("normalize-space(//span[@class=' IconWithCount__count js--IconWithCount__count']/text())").get(),
            'price': response.xpath("normalize-space(//span[@class='ProductHeader__price-default_current-price']/text())").get(),
            'spec': spec_dict
        }
