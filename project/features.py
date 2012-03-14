"""
Feature extraction module.
"""
from PyQt4.QtWebKit import QWebElement
import re
def extract_features(prev,curr,nexx):
	topLeft = curr.geometry().topLeft()
	print (topLeft.x(),topLeft.y())
	bgColor = curr.styleProperty("background-color",QWebElement.ComputedStyle)
	fgColor = curr.styleProperty("color",QWebElement.ComputedStyle)
	print extract_colour(bgColor),extract_colour(fgColor)


rgb_matcher = re.compile("\w+\((\d*), (\d*), (\d*)(, (\d*))?\)")
def extract_colour(color):
	print "'"+color+"'"
	m = rgb_matcher.match(color)
	if m:
		str_tup = m.groups()
		return (int(str_tup[0]),int(str_tup[1]),int(str_tup[2]))
