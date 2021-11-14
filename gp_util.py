#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:29:25 2021

@author: manu
"""

import array
import random

class graph(object):
    def __init__(self,matrix):
        self._matrix = [array.array('I',row) for row in matrix]
        
    def __getitem__(self,key):
        return self._matrix[key[0]][key[1]]
        
    def __len__(self):
        return len(self._matrix)
            
def objective_function(graph, solution):
    res = 0
    
    for i in range(0,len(graph)-1):
        for j in range(i+1,len(graph)):
            res += abs(solution[i]-solution[j])*graph[i,j]
            
    return res
    
def random_solution(n):
    return random.sample([0]*(n//2)+[1]*(n//2),n-(n%2))

