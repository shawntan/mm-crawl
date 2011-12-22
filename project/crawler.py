#!/usr/bin/env python2
import sys,time
import  urlparse
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView
from threadpool import ThreadPool
from scraper import Scraper

RUNNING_INSTANCES = 2
class Crawler(QObject):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #QWebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.scraperlist = Set()
	def load(self,url):
		self.page.mainFrame().setUrl(QUrl(url))
	
	def loadFinished(self):
		print "Loaded."
		document = self.page.mainFrame().documentElement()
		rows = document.findAll("div.data_table table.sdt tbody tr td a")
		for a in rows:
			url = "http://www.boxoffice.com%s"%a.attribute("href")
			split = urlparse.urlsplit(url)
			outfile = "output/%s.csv"%split.path.split("/")[-1]
			self.scraperlist.add(Scraper(self,url,outfile))
		for _ in range(0,5):
			s = self.scraperlist.pop()
			s.start()
			self.scraperlist.add(s)
	def completed(self,scraper):
		try:
			self.scraperlist.remove(scraper)
			
			s = self.scraperlist.pop()
			s.start()
			self.scraperlist.add(s)
		except KeyError:
			print "Set empty."
			sys.exit()
crawler = Crawler()
crawler.load("http://www.boxoffice.com/statistics/alltime_numbers/domestic/data")
crawler.app.exec_()	
