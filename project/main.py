#!/usr/bin/env python2
import sys,os
import  urlparse
from sets import Set
from scraper import Scraper
from PyQt4.QtGui import QApplication
import signal

SCRAPER_POOL = 2

FILE = open('scrap','r')
urlset = Set()

print "Loading urls from file."
while True:
	line = FILE.readline()
	if line:
		urlset.add(line)
	else: break
urlcount = len(urlset)
print urlcount
app = QApplication(sys.argv)
def fetchNext(self):
	global urlcount
	urlcount = urlcount - 1
	try:
		while True:
			url = "http://www.boxoffice.com%s"%urlset.pop().strip()
			
			split = urlparse.urlsplit(url)
			outfile = "output/%s.csv"%split.path.strip().split("/")[-1]
			if os.path.exists(outfile):
				urlcount -= 1
				print "File already exists. Getting next..."
			else:
				break
		
		self.scrape(url,outfile)
	except KeyError:
		if urlcount == 0: sys.exit()

print "Initialising scrapers"
for _ in range(0,SCRAPER_POOL):
	s = Scraper(app,fetchNext)
	try:
		while True:
			url = "http://www.boxoffice.com%s"%urlset.pop().strip()
			split = urlparse.urlsplit(url)
			outfile = "output/%s.csv"%split.path.strip().split("/")[-1]
			if os.path.exists(outfile):
				print "File already exists. Getting next..."
				urlcount -= 1
			else:
				break
		
		s.scrape(url,outfile)
	except KeyError:
		if urlcount == 0: sys.exit()

signal.signal(signal.SIGINT, signal.SIG_DFL)
app.exec_()
