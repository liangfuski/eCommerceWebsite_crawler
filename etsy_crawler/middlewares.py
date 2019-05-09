# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from ua import user_agents
import random
from stem import Signal
from stem.control import Controller
import urllib2
import time

class EtsyCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class EtsyCrawlerDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        # request.headers['User-Agent'] = random.choice(user_agents)
        # textbook used setdefault instead , i think it isn't correct as request.headers['User-Agent'] has already been
        # assigned with 'Scrapy/1.5.1(+https://scrapy.org)'
        # we don't use this when we are using splashrequest because , request.header in this case means the headers
        # send to splash but not the remote destination website . In order to make splash to send responding headers to
        # remote site will have to send the http api to splash for the assignment.
        # see the explanation at https://stackoverflow.com/questions/53132597/running-scrapy-splash-with-proxies
        if request.meta.get('splash', None):
          request.meta['splash']['args']['headers']['User-Agent'] = random.choice(user_agents)
        else:
          request.headers['User-Agent'] = random.choice(user_agents)


        # This if statement is used to extinguish between the image downloading request in MyEstyImagesPipeline and other splash request



class ProxyMiddleware(object):

    def __init__(self, proxy_address):
        self.proxy_address = proxy_address

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('PROXY_ADDRESS'):  # check if there is PROXY_ADDRESS assigned in setting.py
            raise AttributeError
        return cls(crawler.settings.PROXY_ADDRESS)  # __int__ is triggered and crawler.settings.PROXY_ADDRESS will be the param as proxy_address

    def process_request(self, request, spider):
         request.meta['proxy'] = self.proxy_address  # request.meta['proxy'] is a default key of meta , saving the detail of proxy if enable


class TorProxyMiddleware(object):
    """
    Every request will sent to tor-privoxy proxy , the ip in the request header will change every 5 request
    """

    def __init__(self, http_proxy=None, tor_control_port=None, tor_password=None):

        if not http_proxy:
            raise Exception('http proxy setting should not be empty')

        if not tor_control_port:
            raise Exception('tor control port setting should not be empty')

        if not tor_password:
            raise Exception('tor password setting should not be empty')

        self.http_proxy = http_proxy
        self.tor_control_port = tor_control_port
        self.tor_password = tor_password
        self.count = 1
        self.times = 5

    @classmethod
    def from_crawler(cls, crawler):

        http_proxy = crawler.settings.get('HTTP_PROXY')
        tor_control_port = crawler.settings.get('TOR_CONTROL_PORT')
        tor_password = crawler.settings.get('TOR_PASSWORD')

        return cls(http_proxy, tor_control_port, tor_password)

    def process_request(self, request, spider):
        self.count = (self.count + 1) % self.times
        if not self.count:  # if statement will trigger when the process_request has triggered every 5 times
            with Controller.from_port(port=self.tor_control_port) as controller:
                controller.authenticate(password='p709269')
                controller.signal(Signal.NEWNYM)
                time.sleep(controller.get_newnym_wait())
                controller.close()

        if request.meta.get('splash', None):
           # request.meta['proxy'] = self.http_proxy
           # see line 117
           request.meta['splash']['args']['proxy'] = self.http_proxy
        else:
            request.meta['proxy'] = self.http_proxy

        print urllib2.urlopen("http://icanhazip.com/").read()


