#!/bin/python2

m = [
	[1,2,3],
	[4,5,6],
	[7,8,9]
]

I = [
	[1,0,0],
	[0,1,0],
	[0,0,1]
]


def multiply(m1,m2):
	result = []
	for j in range(len(m2)):
		result.append([])
		for i in range(len(m1[0])):
			result[j].append(sum(
				[m1[j][l]*m2[l][i] for l in range(len(m2))]
			))
	return result
				


