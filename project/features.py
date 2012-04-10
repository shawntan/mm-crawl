"""
Feature extraction module.
"""
from PyQt4.QtWebKit import QWebElement
from matrix import *
import random,nltk,string,itertools,re,sys
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

non_alphanum = re.compile('\W') 
number = re.compile('[0-9]')
splitter = re.compile('[\s\.\-\/]+')
stemmer = PorterStemmer()
stop_words = set(nltk.corpus.stopwords.words('english'))


rgb_matcher = re.compile("\w+\((\d*), (\d*), (\d*)(, (\d*))?\)")

"""
store of words found on target pages
"""

def extract_features(curr,seen_elements):

	featup = content_features(curr.nextSibling(),surround_tokens,curr.nextSibling() not in seen_elements) +\
			 content_features(curr.previousSibling(),surround_tokens,curr.previousSibling() not in seen_elements) +\
			 content_features(curr,link_tokens,curr not in seen_elements) +\
			 visual_features(curr)  +\
			 link_features(curr)
	seen_elements.add(curr)
	seen_elements.add(curr.previousSibling())
	seen_elements.add(curr.nextSibling())
	return featup

def document_features(e):
	text_content = unicode(e.toPlainText(),errors="ignore")
	tokens = text_content.split()
	return (len(tokens),len(text_content))

link_tokens = {}
surround_tokens = {}
k = 10
def content_features(e,tokencount,count):
	text_content = unicode(e.toPlainText(),errors="ignore")
	#print text_content
	tokens = text_content.split()
	tokens = [preprocess(w) for w in tokens if preprocess(w)]
	if count:wordcount(e,tokens,tokencount)
	wc_vec = [0]*k
	i=0
	for _,w in get_top_k_words(k,tokencount):
		#print w
		wc_vec[i] = tokens.count(w)
		i+=1
	
	#print "Feature vector "
	#print (len(tokens),len(text_content)) + tuple(wc_vec)
	return (len(tokens),len(text_content)) + tuple(wc_vec)

def preprocess(word):
	w = non_alphanum.sub("",word)
	w = w.lower()
	if w in stop_words: return
	w = stemmer.stem_word(w)
	w = number.sub("",w)
	return w

def get_top_k_words(k,tokencount):
	vocab = [(val,key) for key,val in tokencount.iteritems()]
	vocab.sort()
	return vocab[-k:]

def wordcount(e,tokens,tokencount):
	for i in tokens:tokencount[i] = tokencount.get(i,0) + 1




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

