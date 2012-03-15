#!/usr/bin/python2
from browser import *
from urlparse import urljoin
from features import *
from reward import *
import sys
link_queue = []
visited = set()
def queue_processor(self,curr_url,document):
	try:
		anchors = document.findAll("a")
		for a in anchors:
			try:
				extract_features(a.previousSibling(),a,a.nextSibling())
				href = urljoin(curr_url,str(a.attribute("href")))
				if href not in visited and href.find("ycombinator.com"):
					link_queue.append(href)
					visited.add(href)
			except Exception as ex:
				print ex

	
		print reward(document)
		if link_queue:
			link = link_queue.pop(0)
			print link
			self.load(link)
		else:
			sys.exit()
	except Exception as ex:
		print ex
		sys.exit()

brwsr = Browser(queue_processor)
brwsr.load("http://news.ycombinator.com")
app.exec_()
