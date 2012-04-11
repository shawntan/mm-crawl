#!/usr/bin/python2
import sys

print sys.argv
FILE = open(sys.argv[2],'w')
prev = None
for line in open(sys.argv[1],'r'):
	tup = line.strip().split('\t')
	if prev:
		diff = (float(tup[0]) - float(prev[0]))/60
		if len(prev) >= 2 :
			FILE.write("%d\t%s\n"%(diff,prev[1]))
	prev = tup
