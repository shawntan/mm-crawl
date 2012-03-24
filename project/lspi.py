from matrix import *
import math,random,heapq
DISCOUNT = 0.9
WEIGHT_UPDATE = 10

A = None
b = None
weight = None
prev_bf = None
count = 0

def initialise(n):
	global A,b,weight
	A = Matrix.identity(n)
	b = vector([0]*n)
	weight = Matrix([[1]*n])

def update(reward,curr_bf):
	global A,b,prev_bf,count
	if prev_bf:
		A = A + prev_bf*(prev_bf-DISCOUNT*curr_bf).transpose()
		b = b + reward*prev_bf
	prev_bf = curr_bf
	if count == WEIGHT_UPDATE:
		update_weights()
		count = 0
	else: 
		count += 1

def update_weights():
	global weight,A,b
	print "updating weights..."
	weight = A.eliminate(b).transpose()
	print A
	print b
	print weight

def select_action(vector_list):
	global weight
	if not weight: initialise(len(vector_list[0][1].arr))
	scores = []
	heapq.heapify(scores)
	cum_exp = 0
	for url,vec in vector_list:
		score = (weight*vec).arr[0][0]
		tup = -cum_exp,score,url,vec
		cum_exp += math.exp(score/20)
		heapq.heappush(scores,tup)
	r = random.uniform(0,cum_exp)
	#print "Max " + str(cum_exp)
	exp,s,u,vec = heapq.heappop(scores)
	print u
	while -r > exp and scores:
		#print exp,s,u
		exp,s,u,vec = heapq.heappop(scores)
	#print u,vec
	return u,vec



if __name__ == '__main__':
	"""
	A = Matrix([
		[2.0,0.0,7.0],
		[1.0,1.0,0.0],
		[1.0,0.0,3.0]
	])
	b = vector([1,2,3])
	prev_bf = vector([1,1,2])
	curr_bf = vector([2,1,1])
	A,b = update(A,b,6,prev_bf,curr_bf)
	print A
	print b

	print weights(A,b)
	"""
	test = [(str(a),vector([a+1,a+2,a+3,a+4])) for a in range(0,10)]
	weights = Matrix([[1,1,1,1]])
	for i in range(100):
		print str(select_action(test)) + " is chosen"

