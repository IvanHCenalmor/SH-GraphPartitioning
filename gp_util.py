#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:29:25 2021

@author: manu
"""
import numpy as np
import random
import sys


class pair(object):
    def __init__(self,v0,v1):
        self.v0 = v0
        self.v1 = v1
    
    def __eq__(self,other):
        return self.v0==other.v0 and self.v1==other.v1
    
    def __hash__(self):
        return (self.v0+self.v1)*(self.v0+self.v1+1)//2+self.v1

def parser(filepath):
    with open(filepath, "r") as f:
        n = int(f.readline())
        m = [[int(i) for i in line.split('   ')[:-1]] for line in f.readlines()]
        return n, np.array(m,dtype="uint16")

def objective_function(graph, solution):
    
    aux_sol = np.array([solution])
    
    A = (1 - aux_sol) * aux_sol.transpose()

    W = A + A.transpose()
    
    return np.sum(graph*W)/2    
    
    
def random_solution(n):
    return np.array(random.sample([True]*(n//2)+[False]*(n//2),n),dtype="bool8")     

def main():
    pass

if __name__=="__main__":
    main()
    