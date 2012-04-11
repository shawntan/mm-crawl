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
	if t_delta > 10:	return "> 6"
	else: 			return "=< 6"

def preprocess(word):
	w = non_alphanum.sub("",word)
	w = w.lower()
	if w in stop_words: return
	w = stemmer.stem_word(w)
	w = number.sub("",w)
	return w

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
bayesclassifier = nltk.NaiveBayesClassifier.train(massaged_instances[len(massaged_instances)-500:])
print bayesclassifier.show_most_informative_features(20)
print nltk.classify.accuracy(bayesclassifier,massaged_instances[:500])


