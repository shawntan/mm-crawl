import sys
from time import sleep as usleep
import urlparse
from PyQt4.QtCore import QObject, QUrl, QEventLoop, SIGNAL, pyqtProperty, pyqtSlot
from PyQt4.QtGui import QApplication
from PyQt4.QtWebKit import QWebPage,QWebView
app = QApplication(sys.argv)
INITIAL_SLEEP = 2
class Browser(QObject):
	def __init__(self,callback):
		QObject.__init__(self,app)
		self.callback = callback
		self.view = QWebView()
		self.page = self.view.page()
		self.page.mainFrame().loadFinished.connect(self.cb)
	def load(self,url):
		self.page.mainFrame().setUrl(QUrl(url))
		self.current_url = url
	def back(self):
		self.view.back()
	def cb(self):
		usleep(INITIAL_SLEEP)
		document = self.page.mainFrame().documentElement()
		self.callback(self,self.current_url,document)

if __name__=="__main__":
	links = []
	def cb(document):
		anchors = document.findAll("a")
		for a in anchors:
			links.append(a)
	b1 = Browser(cb)
	b1.load("http://www.google.com")

def print_links(links):
	for a in links:
		print unicode(a.toPlainText(),errors="ignore")
