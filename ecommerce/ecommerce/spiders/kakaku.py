import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class KakakuSpider(CrawlSpider):
    name = 'kakaku'
    allowed_domains = ['kakaku.com']
    start_urls = [
        'https://kakaku.com/search_results/gaming%20laptop/?act=Input&lid=pc_ksearch_searchbutton_top']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='p-item_visual is-biggerlinkBigger s-biggerlinkHover_alpha']",
                           process_value=lambda link: link.replace(
                               '?lid=pc_ksearch_kakakuitem', 'spec'),
                           allow=r"^https://kakaku.com/item"),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths="//li[@class='p-pager_btn p-pager_btn_next']/a"))
    )

    def parse_item(self, response):
        spec_dict = {}
        specs = response.xpath("//th[@class='itemviewColor03b textL']")
        for spec in specs:
            key = spec.xpath(".//text()").get().strip()
            if key:
                spec_dict[key] = spec.xpath(
                    ".//following-sibling::td[1]/text()").get()

        yield {
            'title': response.xpath("//h2/text()").get(),
            'price': response.xpath("//span[@class='priceTxt']/text()").get(),
            'spec': spec_dict
        }
