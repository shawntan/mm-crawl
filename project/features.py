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
splitter = re.compile('[\s\.\-\/\?\&\=\_]+')
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
			 link_features(curr)
			 #visual_features(curr)  +\
	seen_elements.add(curr)
	seen_elements.add(curr.parent())
	return featup

doc_tokens = {}
def document_features(e):
	print get_top_k_words(10,link_tokens)
	print get_top_k_words(10,surround_tokens)
	print get_top_k_words(10,url_tokens)
	print get_top_k_words(10,doc_tokens)
	text_content = unicode(e.toPlainText(),errors="ignore")
	tokens = text_content.split()
	return (len(tokens),len(text_content)) + content_features(e,doc_tokens,True)

link_tokens = {}
surround_tokens = {}
k = 10
count = 0

def content_features(e,tokencount,count):
	text_content = unicode(e.toPlainText(),errors="ignore")
	#print text_content
	tokens = text_content.split()
	tokens = [preprocess(w) for w in tokens if preprocess(w)]
	if count:wordcount(e,tokens,tokencount)
	wc_vec = [0]*k
	i=0
	for w in get_top_k_words(k,tokencount):
		wc_vec[i] = 1 if w in tokens else 0
		i+=1
	
	#print "Feature vector " (len(tokens),len(text_content)) +
	return  tuple(wc_vec)

def preprocess(word):
	w = non_alphanum.sub("",word)
	w = w.lower()
	if w in stop_words: return
	elif w in ["ycombinator","news","http","com","www"]:return
	w = stemmer.stem_word(w)
	w = number.sub("",w)
	if len(w) < 3: return
	return w

def get_top_k_words(k,tokencount):
	vocab = [(val,key) for key,val in tokencount.iteritems()]
	vocab.sort()
	t = [w for _,w in vocab[-k:]]
	t.sort()
	return t

def wordcount(e,tokens,tokencount):
	global count
	if count > 2000: return
	for i in tokens:tokencount[i] = tokencount.get(i,0) + 1
	count +=1
url_tokens = {}
def link_features(e):
	href = str(e.attribute("href"))
	sl_cnt = href.count('/')
	param_cnt = href.count('&') + href.count('?')

	tokens = splitter.split(href)
	tokens = [preprocess(w) for w in tokens if preprocess(w)]
	wordcount(None,tokens,url_tokens)
	wc_vec = [0]*k
	i=0
	for w in get_top_k_words(k,url_tokens):
		wc_vec[i] = 1 if w in tokens else 0
		i+=1
	#(sl_cnt,param_cnt) + 
	return tuple(wc_vec)

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

