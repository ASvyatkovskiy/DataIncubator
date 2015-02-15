#!/usr/bin/env python

itable = open('hits.csv').readlines()

for line in range(1000):  #len(itable)): #range(itable):
    print "('"+itable[line].split(',')[0]+"',"+itable[line].split(',')[1]+","+itable[line].split(',')[2].rstrip()+"),"
