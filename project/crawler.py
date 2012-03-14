#!/usr/bin/python2
from browser import *
from urlparse import urljoin
from features import *
link_queue = []
visited = set()
def queue_processor(self,curr_url,document):
	anchors = document.findAll("a")
	for a in anchors:
		extract_features(a.previousSibling(),a,a.nextSibling())
		href = urljoin(curr_url,str(a.attribute("href")))
		if href not in visited:
			link_queue.append(href)
			visited.add(href)
	if link_queue:
		link = link_queue.pop(0)
		print link
		self.load(link)
	else:
		sys.exit()

brwsr = Browser(queue_processor)
brwsr.load("http://www.slashdot.org")
app.exec_()
