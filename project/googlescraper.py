#!/usr/bin/env python2
import sys,time
import  urlparse,random
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView
from threadpool import ThreadPool
from scraper import Scraper

RUNNING_INSTANCES = 2
class GoogleScraper(QObject):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #QWebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.view.show()
		self.movies = Set()
		
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
		rows = document.findAll("h3.r a.l")
		nextbtn = document.findFirst("a#pnnext")
		for a in rows:
			print a.attribute("href")
			self.movies.add(a.attribute("href"))
		if nextbtn.tagName():
			usleep(random.randint(20,300))
			nextbtn.evaluateJavaScript("this.click()")
		else:
			self.writeToFile()

	
	def writeToFile(self):
		print "Writing to file..."
		file = open('ggmovie.lst', 'w')
		for a in self.movies:
			file.write('%s\n'%a)
		file.close()
		
googlescraper = GoogleScraper()
googlescraper.load("http://www.google.com/search?q=site:www.boxoffice.com/statistics/movies/")
googlescraper.app.exec_()	
