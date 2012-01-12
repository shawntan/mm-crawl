#!/bin/python2

import sys
class Matrix:
	def __init__(self,arr):
		self.arr = arr
	def __mul__(self,other):
		return self.mmult(self.arr,other.arr) if isinstance(other,Matrix) else self.smult(other,self.arr)
	def __rmul__(self, other):
		return other.__mul__(self) if isinstance(other,Matrix) else self.smult(other,self.arr)
	def __add__(self,other):
		def plus(a,b): return a+b
		return self.scalar(self.arr, other.arr,plus)
	def __sub__(self,other):
		def sub(a,b): return a-b
		return self.scalar(self.arr, other.arr,sub)
	def transpose(self):
		result = []
		for i in range(len(self.arr[0])):
			result.append([])
			for j in range(len(self.arr)):
				result[i].append(self.arr[j][i])
		return Matrix(result)


	def scalar(self,m1,m2,op):
		result = []
		for j in range(len(m1)):
			result.append([])
			for i in range(len(m1[0])):
				result[j].append(op(m1[j][i],m2[j][i]))
		return Matrix(result)
	def mmult(self,m1,m2):
		if len(m1[0]) != len(m2): return None
		result = []
		for j in range(len(m1)):
			result.append([])
			for i in range(len(m2[0])):
				result[j].append(sum(
					[m1[j][l]*m2[l][i] for l in range(len(m2))]
				))
		return Matrix(result)
	
	def smult(self,k,m2):
		return Matrix([[k*v for v in r] for r in m2])
		
	def __str__(self):
		out = ''
		for r in self.arr:
			for c in r:
				out += '%d '%c
			out += '\n'
		return out

m = Matrix([
	[1,2,3],
	[4,5,6],
	[4,5,6]
])

I = Matrix([
	[1,0,0],
	[0,1,0],
	[0,0,1]
])


				


