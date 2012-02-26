from matrix import *
DISCOUNT = 0.65
def update(A,b,reward,prev_bf,curr_bf):
	A = A + prev_bf*(prev_bf-DISCOUNT*curr_bf).transpose()
	b = b + reward*prev_bf
	return A,b

def weights(A,b):
	return A.eliminate(b)

if __name__ == '__main__':
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
