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
	doc_fvec = document_features(document)
	a_ft_len = None
	for a in anchors:
		try:
			a_ft = extract_features(a.previousSibling(),a,a.nextSibling())
			a_ft_len = len(a_ft)
			fvec = vector(doc_fvec+ a_ft + (0,))
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
		if history_stack:
			#count fvec length
			back_fvec = vector(doc_fvec + a_ft_len*(0,) + (1,))
			link_queue.append((history_stack[-1],back_fvec))
		link,vec = select_action(link_queue)
		if not visited_before:
			r = reward(document)
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
