#!/usr/bin/env python2
import sys,time
import  urlparse
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView

RUNNING_INSTANCES = 5
class Crawler(QObject):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #Q	WebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.pagelist = Set()
		self.movies = Set()
		self.first = True
		self.count = 0
	def load(self,url):
		self.page.mainFrame().setUrl(QUrl(url))
	
	def loadFinished(self):
		document = self.page.mainFrame().documentElement()
		if self.first:
			links = document.findAll("ul#data_nav li a")
			for a in links:
				self.pagelist.add(a.attribute("href"))
			self.first = False
		else:
			rows = document.findAll("div.data_table table.sdt tbody tr td a")
			for a in rows:
				self.movies.add(a.attribute("href"))
		'''
		try:
			url = self.pagelist.pop()
			print "loading %s"%url
			self.load(url)
		except KeyError:
			print "Set empty!"
			file = open('movieurls.lst', 'w')
			for a in self.movies:
				file.write('%s\n'%a)
			file.close()
		'''
			
crawler = Crawler()
crawler.load("http://www.boxoffice.com/statistics/alltime_numbers/domestic/data")
crawler.app.exec_()	
