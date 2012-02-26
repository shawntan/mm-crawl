#!/bin/python2
import sys
from copy import deepcopy

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
		if len(m1) != len(m2) or len(m1[0]) != len(m2[0]): raise Exception("Wrong dimensions.")
		result = []
		for j in range(len(m1)):
			result.append([])
			for i in range(len(m1[0])):
				result[j].append(op(m1[j][i],m2[j][i]))
		return Matrix(result)
	def mmult(self,m1,m2):
		if len(m1[0]) != len(m2) or len(m2[0]) != len(m1):
			raise Exception("Wrong dimensions")
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
				out += '%0.2f '%c
			out += '\n'
		return out
	
	def eliminate(self,other):
		clone,result = Matrix(deepcopy(self.arr)),Matrix(deepcopy(other.arr))
		m1,m2 = clone.arr,result.arr
		if len(m1) != len(m2): raise Exception("Wrong dimensions")
		for col in range(len(m1[0])):
			nonzero = (i for i in range(col,len(m1)) if m1[i][col]!=0).next()
			factor = 1.0/float(m1[nonzero][col])
			clone.swap_row(nonzero,col)
			result.swap_row(nonzero,col)
			clone.multiply_row(factor,col)
			result.multiply_row(factor,col)
			for row in range(col+1,len(m1)):
				if m1[row][col] != 0:
					fac = m1[row][col]
					clone.add_multiple_of_row(row,col,-fac)
					result.add_multiple_of_row(row,col,-fac)
		for col in reversed(range(1,len(m1[0]))):
			for row in reversed(range(col)):
				if m1[row][col] != 0:
					fac = m1[row][col]
					clone.add_multiple_of_row(row,col,-fac)
					result.add_multiple_of_row(row,col,-fac)
		return result
			
	def swap_row(self,src,desc):
		self.arr[src],self.arr[desc] = self.arr[desc],self.arr[src]
	def multiply_row(self, factor, row):
		self.arr[row] = [factor*i for i in self.arr[row]]
	def add_multiple_of_row(self,r1,r2,factor):
		self.arr[r1] = [
			self.arr[r1][i] + factor*self.arr[r2][i]
			for i in range(len(self.arr[r1]))
		]
	@staticmethod
	def identity(n):
		return Matrix([[0 if j!=i else 1 for i in range(n) ] for j in range(n)])
	def __repr__(self):
		return 'Matrix(%s)'%(self.arr.__repr__())

def vector(l):
	return Matrix([[i] for i in l])



 
