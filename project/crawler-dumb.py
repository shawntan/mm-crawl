#!/usr/bin/python2
from browser import *
from urlparse import urljoin
from features import *
from reward import *
from lspi import *
import sys,random

visited = set()
history_stack = []

LOG = open('noob-crawler.log','w')
cost = 0
targets = 0


link_queue = []
a_ft_len = None
def queue_processor(self,curr_url,document):
	global a_ft_len,cost,targets,LOG
	print "=========================================================================="
	print "\tcurrently at %s"%curr_url

	visited_before = curr_url in visited
	visited.add(curr_url)
	"""
	try:
	"""
	anchors = document.findAll("a")
	doc_fvec = document_features(document)

	if a_ft_len:
		back_fvec = vector(doc_fvec + a_ft_len*(0,) + (1,))
		link_queue.append(("back",back_fvec))

	seen_elements = set()
	for a in anchors:
		try:
			a_ft = extract_features(a,seen_elements)
			a_ft_len = len(a_ft)
			#fvec = vector(doc_fvec+ a_ft + (0,))
			url = str(a.attribute("href")).split('#')[0]
			href = urljoin(curr_url,url)
			if href not in visited\
			and href.find("news.ycombinator.com") >= 0\
			and not href.endswith("jpg")\
			and not href.endswith("gif")\
			and not href.endswith("png")\
			and href.startswith("http:"):
				link_queue.append((href,[]))
		except Exception as ex:
			print ex

	#count fvec length
	
	link,vec = link_queue.pop(0)

	if not visited_before:
		cost += 1
		r = reward(document)
		if r > 5: targets += 1
		#update(r,vec)
	else:
		pass
		#update(-1,vec)
	
	try:
		LOG.write("%d\t%d\n"%(cost,targets))
		LOG.flush()
	except Exception as e:
		print e

	print "Action to take: %s"%link
	#history_stack.append(curr_url)
	if link == "back": self.back()
	else:self.load(link)
	"""
	except Exception as ex:
		print ex
		sys.exit()
	"""
	print "=========================================================================="
brwsr = Browser(queue_processor)
brwsr.load("http://news.ycombinator.com")
app.exec_()
