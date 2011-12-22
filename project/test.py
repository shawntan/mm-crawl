#!/usr/bin/env python2
from scraper import Scraper
from PyQt4.QtGui import QApplication
import sys


app = QApplication(sys.argv)
def dummy(self):
	print "Stupid method"
scraper = Scraper(app,dummy)
scraper.scrape("http://www.boxoffice.com/statistics/movies/fast-five-2011","test.csv")
app.exec_()


