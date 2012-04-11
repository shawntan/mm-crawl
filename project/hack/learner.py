#!/usr/bin/python2
# -*- coding: utf-8 -*-
import random,nltk,string,itertools
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
from nltk.stem.porter import PorterStemmer
web_words = ['www','http','ftp','com','html','org']
eng_stopwords = stopwords.words('english')
stemmer = PorterStemmer()
class Classifier(object):
	total_docs = 0
	categories = {}
	cat_gram_freq = {}
	cat_word_freq = {}
	vocab = set()
	def __init__(self,root):
		print "Building model..."
		self.train_classifier(root)
		print "Done."
	def load_documents(self,path):
		docs = CategorizedPlaintextCorpusReader(path,r'.*/.*',cat_pattern=r'(.*)/.*')
		for cat in docs.categories():
			self.cat_gram_freq[cat] = {}
			self.cat_word_freq[cat]={}
		return ((category,list(docs.words(fileid))) 
			for category in docs.categories() 
			for fileid in docs.fileids(category))

	def extract_bigrams(self,doc):
		return (i for i in nltk.bigrams(doc))
		
	def train_classifier(self,root):
		#massage the data in.
		documents = self.load_documents(root)
		for cat,doc in documents:
			self.total_docs += 1
			self.categories[cat] = self.categories.get(cat,0) + 1
			word_freq = self.cat_word_freq[cat]
			bigrams_freq = self.cat_gram_freq[cat]
			for i,j in self.extract_bigrams(doc):
				i,j = filter_word(i),filter_word(j)
				if i and j:
					word_freq[i] = word_freq.get(i,0) + 1
					first_word = bigrams_freq.setdefault(i,{})
					first_word[j] = first_word.get(j,0) + 1
					self.vocab.add(i)
		#print self.total_docs
		#print self.categories
	def classify(self,doc):
		category,prob = None,-1
		vocab  = len(self.vocab)
		for cat in self.cat_gram_freq:
			word_freq = self.cat_word_freq[cat]
			bigrams_freq = self.cat_gram_freq[cat]
			tot_prob = 1 #float(self.categories[cat])/float(self.total_docs)
			for i,j in self.extract_bigrams(doc):
				i,j = filter_word(i),filter_word(j)
				if i and j:
					if i in bigrams_freq:
						if j in bigrams_freq[i]:
							bi_freq = bigrams_freq[i][j]
						else:
							bi_freq = 0
						p = float(bi_freq+1)/float(word_freq[i] + vocab)
					else:
						p = 1/float(vocab)
					#print i,j,p
					tot_prob *= p
			if tot_prob >= prob:
				category,prob = cat,tot_prob
			#print "\t%s %0.40f"%(cat,tot_prob)
		return category
def filter_word(word):
	if word in web_words or word in eng_stopwords: return
	if not word.isalpha(): return
	if len(word) <= 2: return
	word = word.lower()
	word = stemmer.stem_word(word)
	return word
if __name__=="__main__":
	clsfr = Classifier('train')
	

