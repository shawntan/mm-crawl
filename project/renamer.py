#!/usr/bin/env python2
import sys,os

for fn in os.listdir("output"):
	FILE = open("output/%s"%fn,'r')
	attributecount = len(FILE.readline().split(','))-1;
	df = "n"
	if FILE.readline().split(',')[0].startswith('"\''):
		df="r"
	FILE.close()
	os.rename("output/%s"%fn,"output/%s%02d_%s"%(df,attributecount,fn))
	
