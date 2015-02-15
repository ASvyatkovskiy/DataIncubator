#!/usr/bin/env python

import numpy as np
from random import randint
import datetime
import time


#1. consider a row of seats as a boolean array isOccupied[N] initialized to false (not occupied) 
#2. generate (uniform) random integer j in the range [1,N]
#3. if not (isOccupied[j-1] || isOccupied[j] || isOccupied[j+1]), i.e. j or adjacent seats are not occupied, set isOccupied[j] = true
#4. in case it is occupied and the capacity is less or equal to some expected threshold repeat step 2) 


def isOccupiedCheck(listOfSeats,index):
    if index == listOfSeats.shape[0]-1: return listOfSeats[index-1] or listOfSeats[index]
    elif index == 0: return listOfSeats[index] or listOfSeats[index+1]
    else: return listOfSeats[index-1] or listOfSeats[index] or listOfSeats[index+1]

def fractionVisited(isVisited):
    return sum(isVisited)/isVisited.shape[0]

def getReplica(epsilon,N):
    isOccupied = np.zeros(N)
    isVisited = np.zeros(N)

    #while the capacity is not reached
    while fractionVisited(isVisited) < epsilon:
        seatIndex = randint(0,N-1)
        #if it was alrady visited, nompoint checking again
        if isVisited[seatIndex] == 1: continue
        if not isOccupiedCheck(isOccupied,seatIndex):
            #seat the passenger
            isOccupied[seatIndex] = 1
        isVisited[seatIndex] = 1

    #print "Fraction of occupied seats for N = ", N, " is ", sum(isOccupied)/isOccupied.shape[0]
    return sum(isOccupied)/isOccupied.shape[0]

epsilon = 0.99999999 #0.98
N = 25
Nreplicas = 1000
replicas = np.zeros(Nreplicas)


from joblib import Parallel, delayed  
import multiprocessing

# what are your inputs, and what operation do you want to 
# perform on each input. For example...

t0 = time.clock()
inputs = range(Nreplicas)
num_cores = multiprocessing.cpu_count()
print "Running on ", num_cores, " CPU cores"
replicas = Parallel(n_jobs=num_cores)(delayed(getReplica)(epsilon,N) for i in inputs)  

#serial implementation
#for irep in range(Nreplicas):
#    #print "Analyzing replica ", irep, " ", datetime.datetime.now()
#    replicas[irep] = getReplica(epsilon,N)
print time.clock() - t0, "seconds process time"


#after the capacity is reached, check the fraction of 1s to the total size of the array to get rho
print "N ", N, " Nreplicas ", Nreplicas, " epsilon ",epsilon
print "For experiment with N seats = ", N, " having repeated with ", Nreplicas, " MC replicas"
print "Mean occupancy fraction: ", np.mean(replicas)
print "Standard deviation of occupancy fraction: ", np.std(replicas)  
