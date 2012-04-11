#!/usr/bin/python2
# -*- coding: utf-8 -*-
# author: Rolando Espinoza La fuente
#
# Changelog:
#     24/07/2011 - updated to work with scrapy 13.0dev
#     25/08/2010 - initial version. works with scrapy 0.9

from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from urlparse import urljoin
import itertools
import time
import sys
"""
/tr[1]/td[1][contains(concat(' ',@class,' '),' thead ')]
/tr[2]/td[2][last()][contains(concat(' ',@class,' '),' alt1 ')]/div[1]
"""

URL = sys.argv[1]
LOG_NAME = URL.split("/")[-1].split(".")[0]
LOG = open('%s.log'%LOG_NAME,'w')
class MySpider(BaseSpider):
	"""Our ad-hoc spider"""
	name = "myspider"
	#start_urls = ["http://forums.hardwarezone.com.sg/eat-drink-man-woman-16/come-talk-about-all-ur-r-s-problems-part-7-a-3662918.html"]
	start_urls = [URL]
	next_links =  "//li[contains(concat(' ',@class,' '),' prevnext ')]//a[contains(text(),'Next')]/@href"
	entries = "//div[@id='posts']/div[contains(concat(' ',@class,' '),' post-wrapper ')]/table[contains(concat(' ',@class,' '),' post ')]"
	visited = set()
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		forum_links = itertools.chain(
						hxs.select(self.next_links))
		qxs = forum_links.next()
		url = urljoin(response.url,qxs.extract())
		if url not in self.visited:
			yield self.make_requests_from_url(url)
		"""
		for qxs in forum_links:
			url = urljoin(response.url,qxs.extract())
			if url not in self.visited:
				yield self.make_requests_from_url(url)
		"""
		for qxs in hxs.select(self.entries):
			timestr = ''.join([i.extract() for i in\
						iter(qxs.select("..//tr[1]/td[1][contains(concat(' ',@class,' '),' thead ')]/text()"))]).strip()
			t = time.strptime(timestr,"%d-%m-%Y, %I:%M %p")
			tup = "%s\t%s"%(
				str(time.mktime(t)),
				''.join([i.extract().replace('\n',' ').replace('\r',' ') for i in\
						iter(qxs.select(".//tr[2]/td[2][last()][contains(concat(' ',@class,' '),' alt1 ')]/div[1]/text()"))]).strip()
			)
			LOG.write(tup + "\n")
def main():
	"""Setups item signal and run the spider"""
	# set up signal to catch items scraped
	from scrapy import signals
	from scrapy.xlib.pydispatch import dispatcher

	def catch_item(sender, item, **kwargs):
		print "Got:", item

	dispatcher.connect(catch_item, signal=signals.item_passed)

	# shut off log
	from scrapy.conf import settings
	settings.overrides['LOG_ENABLED'] = False

	# set up crawler
	from scrapy.crawler import CrawlerProcess

	crawler = CrawlerProcess(settings)
	crawler.install()
	crawler.configure()

	# schedule spider
	spider = MySpider()
	crawler.queue.append_spider(spider)
	#crawler.crawl(MySpider())

	# start engine scrapy/twisted
#	print "STARTING ENGINE"
	crawler.start()
#	print "ENGINE STOPPED"

if __name__ == '__main__':
	main()
