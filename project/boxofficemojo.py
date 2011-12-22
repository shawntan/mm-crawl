#!/usr/bin/env python2
import sys,time
import  urlparse,random,codecs
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView
from threadpool import ThreadPool
from scraper import Scraper

RUNNING_INSTANCES = 2
page = ['NUM',
		'A','B','C','D','E',
		'F','G','H','I','J',
		'K','L','M','N','O',
		'P','Q','R','S','T',
		'U','V','W','X','Y',
		'Z']
class BOMScraper(QObject):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #QWebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.view.show()
		self.movies = Set()
		self.alpha = 0
		self.i = 1
	def load(self,url):
		self.page.mainFrame().setUrl(QUrl(url))
	
	def loadFinished(self):	
		document = self.page.mainFrame().documentElement()
		document.evaluateJavaScript("""
			var evt = document.createEvent('MouseEvents');
			evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
			Element.prototype.click = function() {
				this.dispatchEvent(evt);
			};
		""")
		rows = document.findAll("table table table tbody td a b")
		if rows:
			for a in rows:
				strfied = unicode(a.toInnerXml())
				self.movies.add(strfied)
				print unicode(a.toInnerXml())
			if document.findFirst("table:nth-child(4) tbody tr td font b a").tagName():				
				self.i = self.i + 1
			else:
				self.alpha = self.alpha + 1
				self.i = 1
		else:
			
			self.alpha = self.alpha + 1

			self.i = 1

		if(self.alpha == len(page)):
			self.writeToFile()
		else:
			newurl = "http://boxofficemojo.com/movies/alphabetical.htm?letter=%s&page=%d&p=.htm"%(page[self.alpha],self.i)
			print newurl
			self.load(newurl)
	def writeToFile(self):
		print "Writing to file..."
		file = codecs.open('moviename.lst', encoding='utf-8', mode='w+')
		for a in self.movies:
			file.write('%s\n'%a)
		file.close()
		sys.exit()
bscraper = BOMScraper()
bscraper.load("http://boxofficemojo.com/movies/alphabetical.htm?letter=NUM&page=1&p=.htm")
bscraper.app.exec_()	
