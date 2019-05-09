# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider, Rule
from ..items import EtsyCrawlerItem
from scrapy_splash import SplashRequest
from scrapy.linkextractor import LinkExtractor
import base64
import re
from lua import splash_args2, lua_script1
from etsy_cookies import etsycookies
import pprint

class EtsySpider(CrawlSpider):

    name = 'etsy'
    allowed_domains = ['']
    start_urls = ['']

    # process_request is used to process the request of the extracted link , see self._request_to_follow
    # callback is the function to parse the web page of the extracted link
    # note that Rule class's constructor takes in three three function argument , which call be assigned as
    # a callable e.g callback = self.method , or a string e.g callable = 'method'
    rules = (Rule(LinkExtractor(allow=('1814991&order=date_desc&ref=pagination&page=',)), follow=False,
                  process_request='splash_request', callback='parse_products_page'),
             )

    # start_requests is overwritten to construct a SplashRequest
    def start_requests(self):
        splash_args = {
            'wait': 3,
            'lua_source': lua_script1,
            'cookies': etsycookies
        }
        for url in self.start_urls:
            yield SplashRequest(url,
                                callback=self.parse,
                                headers={'Referer': 'https://www.etsy.com/c/jewelry?explicit=1'},
                                # when i try request.meta['splash']['args']['proxy'] = self.http_proxy at middlewares , error occurs
                                endpoint='execute',
                                args=splash_args)

    # this is just the default parse method of CrawSpider Class
    def parse(self, response):
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True, )

    # The start_urls web page is parsed by self.parse_product_page
    def parse_start_url(self, response):
        return self.parse_products_page(response)

    # This method used to process the request of Links object in links in _requests_to_follow method . The original
    # request is a normal request
    # In order to make the request behave like a splash request , we add staffs to 'splash' key of request.meta

    def splash_request(self, request):
        request.meta['splash'] = {}    # declare request.meta['splash'] is a dictionary
        request.meta['splash']['args'] = {'wait': 5,
                                          'headers': {'Referer':'https://www.etsy.com/c/jewelry?explicit=1'},
                                          'lua_source': lua_script1,
                                          'cookies': etsycookies
                                          }
        request.meta['splash']['endpoint'] = 'execute'
        return request

    def _requests_to_follow(self, response):
        """
        The following if statement from the default script is removed because the response is a Splash Response

        if not isinstance(response, HtmlResponse):
            return
        """
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def parse_products_page(self, response):
        self.logger.info(pprint.pformat(response.data['har']))
        product_element_lists = response.xpath('//*[@id="reorderable-listing-results"]/li')

        for product_element in product_element_lists:

            review_num_str = product_element.xpath(
                './div/a/div[2]/div/p/span[1]/span[2]/span[2]/text()').extract_first()  # since this is the second time applying xpath on the same path the query should start with nth or './ '
                                                                                        # trying '//div'  will not only extract a product_element's but other members in product_element_lists
                                                                                        # try './/div' instead

            # review_num_str may return None , as the product don't have review, which cannot be the parameter for int()
            if review_num_str:
                np = re.compile(r'\d')
                review_number = int(''.join(np.findall(review_num_str)))
            else:
                review_number = 0

            if review_number >= 500:
                item = EtsyCrawlerItem()
                item['product_name'] = ' '.join(product_element.xpath('div/a/div[2]/div/h2/text()').re(r'\w+[,%+-]*'))
                item['price'] = ''.join(product_element.xpath(
                    './/p/span[2]/span/text()').extract())  # all the texts in the span tags which are children of span[2] are put
                item['shop'] = product_element.xpath(
                    './/p/span[1]/span[1]/text()').extract_first()  # into a list , and then join together to form a str

                product_url = product_element.xpath('.//a[contains(@href,"listing")]/@href').extract_first()
                request = SplashRequest(product_url, self.parse_product_page,
                                        endpoint='execute', args=splash_args2)
                request.meta['item'] = item
                return request
                # since the endpoint is execute , the response is a SplashJsonResponse

    def parse_product_page(self, response):

        self.logger.info(pprint.pformat(response.data['har']))
        item = response.meta['item']

        item['screenshot'] = base64.b64decode(response.data['screenshot'])
        item['link'] = response.url
        item['image_urls'] = response.xpath('//li[contains(@id,"image")]/@data-large-image-href').extract()

        fee = ''.join(response.xpath(
            '//*[@id="estimated-shipping-variant"]//div/span/text()').extract())

        item['shipping_fee_to_cali'] = fee if fee else 'free'

        part = re.compile(r'/listing/(\d+)/')
        item['id'] = part.search(response.url).group(1)

        yield item
