# -*- coding: utf-8 -*-

# Scrapy settings for etsy_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'etsy_crawler'

SPIDER_MODULES = ['etsy_crawler.spiders']
NEWSPIDER_MODULE = 'etsy_crawler.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'etsy_crawler (+http://www.yourdomain.com)'

'''
Normally we obey robots.txt rules,
however , etsy's robots.txt will however allow us to crawl , 
so we set it to False
'''

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 3
# CONCURRENT_REQUESTS_PER_IP = 16
'''
Set this option to a higher value (e.g. 2.0) to increase the throughput 
and the load on remote servers. A lower AUTOTHROTTLE_TARGET_CONCURRENCY value (e.g. 0.5) 
makes the crawler more conservative and polite.
'''
AUTOTHROTTLE_ENABLE = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'etsy_crawler.middlewares.EtsyCrawlerSpiderMiddleware': 543,
#}
SPIDER_MIDDLEWARES = {
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    'etsy_crawler.middlewares.RandomUserAgentMiddleware': 200
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'etsy_crawler.middlewares.EtsyCrawlerDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 750,
    'etsy_crawler.middlewares.RandomUserAgentMiddleware': 800,
    'etsy_crawler.middlewares.TorProxyMiddleware': 888
}
#    'etsy_crawler.middlewares.ProxyMiddleware': 800,
# for setting a distant proxy which is not applicatable in this case  , HTTPPROXY_ENABLED = True , PROXY_ADDRESS = 'http://61.129.70.131:8080'
#    'scrapy.downloadermiddlers.HttpProxyMiddleware': 888,  # see book page 364, another way to generate random ip

# Pirvoxy listening on 8118
HTTP_PROXY = 'http://127.0.0.1:8118'
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = 'p709269'
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'etsy_crawler.pipelines.EtsyCrawlerPipeline': 300,
#}
ITEM_PIPELINES = {'etsy_crawler.pipelines.MyEstyImagesPipeline': None,
                  'etsy_crawler.pipelines.MongoPipeline': 100,
                  'etsy_crawler.pipelines.ScreenShotPipeline': 200
                  }
IMAGES_STORE = '/home/fu/crawler_project/etsy_crawler/item_image'
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

SPLASH_URL = 'http://localhost:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter' , we are using redis dupefilter instead

### HTTPERROR_ALLOWED_CODE = [200, 201, 304]
### HTTPERROR_ALLOW_ALL = False

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500]

DEPTH_LIMIT = 20  # avoiding the recursive loop caused by a honey net


### DUPEFILTER_CLASS = 'etsy_crawler.dupefilter.RedisBloomDupefilter'
### REDIS_DUP_DB = 0
### REDIS_PORT = 6379
### REDIS_KEY = 'Bloom_Filter'
### BLOOMFILTER_BIT = 30
### BLOOMFILTER_HASH_NUMBER = 6

MONGO_URL = 'mongodb+srv://fu_liang:fu2017fu@fu-h0vum.mongodb.net/test?retryWrites=true'
MONGO_DATABASE = "etsy_data"
MONGO_COLLECTION = 'etsy_items'

# DOWNLOADER_CLIENTCONTEXTFACTORY = 'etsy_crawler.customcontextfactory.CustomContextFactory'

LOG_FILE = '/home/fu/crawler_project/etsy_crawler/log.txt'
