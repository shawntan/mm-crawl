#!/usr/bin/python2
# -*- coding: utf-8 -*-
import random,nltk,string,itertools
from nltk.corpus import stopwords
from nltk.corpus import movie_reviews
from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
web_words = ['www','http','ftp','com','html','org']
eng_stopwords = stopwords.words('english')

class Classifier(object):
	def __init__(self,root):
		self.train_classifier(root)
	def load_documents(self,path):
		docs = CategorizedPlaintextCorpusReader(path,r'.*/.*',cat_pattern=r'(.*)/.*')
		print docs.categories()
		documents = [(list(docs.words(fileid)), category)
				for category in docs.categories()
				for fileid in docs.fileids(category)
		]
		random.shuffle(documents)
		return documents

	def document_features(self,document):
		"""
		Creates feature set for all items
		"""
		document_words = set(self.extract_bigrams(document))
		#print document_words
		features={}
		for word in self.doc_features:
			features['has(%s)' % word] = (word in document_words)
		return features

	def extract_bigrams(self,doc):
		return ['-'.join(i) for i in nltk.bigrams(
			w.lower() for w in doc
			if  w.isalpha()
			and len(w) > 2
		) if i[0] not in eng_stopwords
		 and i[1] not in eng_stopwords
		 and i[0] not in web_words
		 and i[1] not in web_words]

	def select_features(self,documents):
		print "Computing bigrams for dataset..."
		#print bigrams
		l =[]
		bigram_dist = nltk.FreqDist(itertools.chain(*(self.extract_bigrams(instance[0]) for instance in documents)))
		return bigram_dist.keys()[:1000]

	def train_classifier(self,root):
		#massage the data in.
		documents = self.load_documents('/home/shawn/project/train')
		self.doc_features = self.select_features(documents)
		featuresets = [(self.document_features(d), c) for (d,c) in documents]
	#for now keep the same
		train_set,test_set = featuresets, featuresets
		bayesclassifier = nltk.NaiveBayesClassifier.train(train_set)
		print bayesclassifier.show_most_informative_features(20)
		print nltk.classify.accuracy(bayesclassifier,test_set)
		self.classifier = bayesclassifier
	def classify(self,doc):
		features = self.document_features(doc)
		#print features
		return self.classifier.classify(features)
if __name__=="__main__":
	clsfr = Classifier('/home/shawn/project/train')
	

