#!/usr/bin/env python2
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

class MySpider(BaseSpider):
	"""Our ad-hoc spider"""
	name = "myspider"
	start_urls = ["http://forums.hardwarezone.com.sg/"]

	forum_links = "//div[@id='forum']/table[3]/tbody/tr/td[contains(concat(' ',@class,' '),' alt1Active ')]/div[1]/a[1]/@href"
	sub_forum_links = "//table[1]//tr[1]/td[3]/div[1]/a[1]/@href"
	next_links = "//form[@id='inlinemodform']/table[4][last()]/tbody[1][last()]/tr[1][last()]/td[2][last()]/div[1][contains(concat(' ',@class,' '),' pagination ')]/ul[1][last()]/li[contains(concat(' ',@class,' '),' prevnext ')]/a[1][last()]/@href"
	entries = "//table[@id='threadslist']/tbody[2][last()]/tr"
	visited = set()
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		forum_links = itertools.chain(
						hxs.select(self.forum_links),
						hxs.select(self.sub_forum_links),
						hxs.select(self.next_links))
		
		for qxs in forum_links:
			url = urljoin(response.url,qxs.extract())
			if url not in self.visited:
				yield self.make_requests_from_url(url)

		for qxs in hxs.select(self.entries):
			print "%s\t%s\t%s"%(
					iter(qxs.select("./td[3]//@href")).next().extract(),
					iter(qxs.select("./td[5]//text()")).next().extract(),
					iter(qxs.select("./td[6]//text()")).next().extract())
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
