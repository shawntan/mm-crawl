#!/usr/bin/python2
import random,nltk,string,itertools,re,sys
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

non_alphanum = re.compile('\W') 
number = re.compile('[0-9]')
splitter = re.compile('[\s\.\-\/]+')
stemmer = PorterStemmer()
stop_words = set(nltk.corpus.stopwords.words('english'))





def preprocess_post(t_delta,text):
	tokens = []
	for i in text.split():
		w = preprocess(i)
		if w:
			tokens.append(w)
	return binnify_t_deltas(t_delta),tokens

def create_instance(features,clazz,doc):
	i = {}
	for f in features: i[f] = (f in doc)
	return i,clazz
	
def binnify_t_deltas(t_delta):
	if t_delta > 6:	return "> 6"
	else: 			return "=< 6"

def preprocess(word):
	w = non_alphanum.sub("",word)
	w = w.lower()
	if w in stop_words: return
#	w = stemmer.stem_word(w)
	w = number.sub("",w)
	return w


if __name__ == "__main__" :
	instances = []
	for line in open(sys.argv[1],'r'):
		tup = line.split('\t')
		instances.append(preprocess_post(int(tup[0]),tup[1]))
	word_dist = nltk.FreqDist(itertools.chain(*(instance[1] for instance in instances if instance[0] == '> 6')))
	features = word_dist.keys()[:500]
	word_dist = nltk.FreqDist(itertools.chain(*(instance[1] for instance in instances if instance[0] == '=< 6')))
	features = word_dist.keys()[:500] + features
	features = set(features)
	massaged_instances = [create_instance(features,instance[0],instance[1]) for instance in instances]
	random.shuffle(massaged_instances)
	
	#cross validation
	k = 10
	set_size = len(massaged_instances)/(k)
	for i in range(k):
		si = i * set_size
		test_set = massaged_instances[si:min(si+set_size,len(massaged_instances)]
		training =  massaged_instances[:si] +\
					massaged_instances[si+set_size:]

		bayesclassifier = nltk.NaiveBayesClassifier.train(training)
		print bayesclassifier.show_most_informative_features(20)
		print nltk.classify.accuracy(bayesclassifier,test_set)
		for cat in ['=< 6','> 6']:
			tp = fp = fn = tn = 0
			for w,c in test_set:
				p = bayesclassifier.classify(w)
				if   p == cat and c == cat: tp += 1
				elif p == cat and c != cat: fp += 1
				elif p != cat and c == cat: fn += 1
				elif p != cat and c != cat: tn += 1
			print "%s count: %d",(tp + fn)
			precision = tp/float(tp+fp)
			recall = tp/float(tp+fn)
			print "%s precision: %0.2f"%(cat,precision)
			print "%s recall: %0.2f"%(cat,recall)
			print "%s F_1: %0.2f"%(cat,2*recall*precision/(recall+precision))
			








