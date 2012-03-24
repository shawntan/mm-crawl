"""
Feature extraction module.
"""
from PyQt4.QtWebKit import QWebElement
import re,sys
from matrix import *
rgb_matcher = re.compile("\w+\((\d*), (\d*), (\d*)(, (\d*))?\)")

def extract_features(prev,curr,nexx):
	featup = content_features(curr) +\
			 visual_features(curr)  +\
			 link_features(curr)
	return featup
def content_features(e):
	text_content = unicode(e.toPlainText(),errors="ignore")
	tokens = text_content.split()
	
	return (len(tokens),len(text_content))

def link_features(e):
	href = str(e.attribute("href"))
	sl_cnt = href.count('/')
	param_cnt = href.count('&') + href.count('?')
	return (sl_cnt,param_cnt)

def visual_features(e):
	topLeft =  e.geometry().topLeft()
	bgColour = e.styleProperty("background-color",QWebElement.ComputedStyle)
	fgColour = e.styleProperty("color",QWebElement.ComputedStyle)

	fgrgb = extract_colour(fgColour)
	bgrgb = extract_colour(bgColour)
	hs = hue_sat(fgrgb,bgrgb)

	return (topLeft.x(),topLeft.y()) + (1,1) + hs


def extract_colour(color):
	m = rgb_matcher.match(color)
	str_tup = m.groups()
	return (int(str_tup[0]),int(str_tup[1]),int(str_tup[2]))

def hue_sat(bgcolor,fgcolor):
	#brightness difference
	bgcol_br = 0.299*bgcolor[0] + 0.587*bgcolor[1] + 0.114*bgcolor[2]
	fgcol_br = 0.299*fgcolor[0] + 0.587*fgcolor[1] + 0.114*fgcolor[2]
	bright_diff = abs(bgcol_br-fgcol_br)
	color_diff = abs(bgcolor[0] - fgcolor[0]) + abs(bgcolor[1] - fgcolor[1]) + abs(bgcolor[2] - fgcolor[2])
	return bright_diff,color_diff

