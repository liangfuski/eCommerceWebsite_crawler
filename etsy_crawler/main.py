from scrapy import cmdline
import os

# os.system('docker run -p 8050:8050 -d scrapinghub/splash')
cmdline.execute("scrapy crawl etsy".split())