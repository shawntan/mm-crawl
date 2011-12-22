#!/usr/bin/env python2
import sys,time,os
import  urlparse
from sets import Set
from time import sleep as usleep
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage, QWebView


class Scraper(QObject):
	def __init__(self,parent,completed):
		self.app = parent
		QObject.__init__(self,self.app)
		self.view = QWebView()
		self.page = self.view.page() #QWebPage(self.app)
		self.page.mainFrame().loadFinished.connect(self.loadFinished)
		self.db = {}
		self.attset = Set()
		self.completed = completed
	def scrape(self,url,outfile):
		del self.db
		del self.attset
		self.db = {}
		self.attset = Set()
		self.db = {}
		self.outfile = outfile
		self.url = url
		self.page.mainFrame().setUrl(QUrl(self.url))
	
	def loadFinished(self):
		print "Loaded %s"%self.url
		document = self.page.mainFrame().documentElement()
		#print unicode(document.toInnerXml())
		document.evaluateJavaScript("""
			var evt = document.createEvent('MouseEvents');
			evt.initMouseEvent('click', true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
			Element.prototype.click = function() {
				this.dispatchEvent(evt);
			};
		""")

		containers = [
			'domestic_data',
			'trailer_fans',
			'twitter_buzzes',
			'daily_count_buzzes',
			'facebook_fans'
		]
		for c in containers:
			container = document.findFirst("#%s"%c)
			attList = self.extractTableHeader(container)
			while True:
				self.extractTableData(container,attList)
				next_btn = container.findFirst("div.pagination a.next_page")
				if next_btn.tagName():
					content = container.toInnerXml()
					next_btn.evaluateJavaScript("this.click()")
					while container.toInnerXml() == content:
						usleep(0.005)
						QApplication.processEvents(QEventLoop.AllEvents, 25)
				else:
					break
		if self.db:
			self.outputFile()
		else:
			print """
			===============================
			Failed extraction! %s
			===============================
			"""%self.url
		print "done %s"%self.url
		self.completed(self)
	
	def outputFile(self):
		split = urlparse.urlsplit(self.url)
		self.outfile = "output/%s.csv"%split.path.strip().split("/")[-1]
		file = open(self.outfile, 'w')
		keylist = self.db.keys()
		keylist.sort()
		rowarr = []
		rowstr = '"Date",'
		for a in self.attset:
			rowstr += '"%s",'%a
			rowarr.append(a)
		file.write(rowstr+'\n')
		
		for k in keylist:
			rowstr = '"%s",'%k
			for a in rowarr:
				if a in self.db[k]:
					rowstr += '"%s",'%self.db[k][a]
				else:
					rowstr += ','	
			file.write(rowstr+'\n')
		file.close()
	def extractTableHeader(self,contentElement):
		tableHead = contentElement.findFirst("table thead tr")
		tmp = tableHead.firstChild()
		attList = []
		while tmp.tagName():
			attList.append(str(tmp.toInnerXml()))
			if str(tmp.toInnerXml()) != 'Date':
				self.attset.add(str(contentElement.attribute('id')+"."+tmp.toInnerXml()))
			tmp = tmp.nextSibling()
		return attList
	def extractTableData(self,contentElement,attList):
		tableBody = contentElement.findAll("table tbody tr")
		for tableRow in tableBody:
			i = 0
			tmp = tableRow.firstChild()
			while tmp.tagName():
				attstr = str(tmp.toInnerXml())
				if attList[i]=='Date':
					try:
						attstr = time.strftime('%Y-%m-%d',time.strptime(str(tmp.toInnerXml()), '%b %d, %Y'))
					except:
						attstr = "'%s"%str(tmp.toInnerXml())
					if attstr in self.db:
						rowtuple = self.db[attstr]
					else:
						rowtuple = {attList[i]:attstr}
						self.db[attstr] = rowtuple
				else:
					rowtuple[str(contentElement.attribute('id'))+"."+attList[i]] = attstr
									
				tmp = tmp.nextSibling()
				i+=1
