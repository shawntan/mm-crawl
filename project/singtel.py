#!/usr/bin/env python2
import sys,time
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView


class Scraper(QObject):
	def __init__(self):
		self.app = QApplication(sys.argv)
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #QWebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.db = {}
		self.attset = Set()
		self.view.show()
	def start(self):
		print "loading %s"%self.url
		self.load(self.url)
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
		print "yay"
		
scraper = Scraper()
scraper.load("http://waccess.singtel.com")
scraper.app.exec_()
