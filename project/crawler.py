#!/usr/bin/python2
from browser import *
from urlparse import urljoin
from features import *
from reward import *
from lspi import *
import sys,random

visited = set()
history_stack = []
def queue_processor(self,curr_url,document):
	visited_before = curr_url in visited
	visited.add(curr_url)
	"""
	try:
	"""
	anchors = document.findAll("a")
	link_queue = []
	for a in anchors:
		try:
			fvec = vector(extract_features(a.previousSibling(),a,a.nextSibling()))
			url = str(a.attribute("href")).split('#')[0]
			href = urljoin(curr_url,url)
			if href not in visited\
			and href.find("ycombinator.com") >= 0\
			and not href.endswith("jpg")\
			and not href.endswith("gif")\
			and not href.endswith("png"):
				link_queue.append((href,fvec))
		except Exception as ex:
			print ex
	if link_queue:
		link,vec = select_action(link_queue)
		if not visited_before:
			r= reward(document)
			update(r,vec)
		history_stack.append(curr_url)
		self.load(link)
	else:
		if history_stack:
			self.load(history_stack.pop())
		else: sys.exit()
	"""
	except Exception as ex:
		print ex
		sys.exit()
	"""
brwsr = Browser(queue_processor)
brwsr.load("http://news.ycombinator.com")
app.exec_()
