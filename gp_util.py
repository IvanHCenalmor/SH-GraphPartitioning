#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:29:25 2021

@author: manu
"""

import array
import random
import sys


class graph(object):
    def __init__(self,matrix):
        self._matrix = [array.array('I',row) for row in matrix]
        
    def __getitem__(self,key):
        return self._matrix[key[0]][key[1]]
        
    def __len__(self):
        return len(self._matrix)

def parser(filepath):
    with open(filepath, "r") as f:
        n = int(f.readline())
        m = [[int(i) for i in line.split('   ')[:-1]] for line in f.readlines()]
        return graph(m)

def objective_function(graph, solution):
    res = 0
    
    for i in range(0,len(graph)-1):
        for j in range(i+1,len(graph)):
            res += abs(solution[i]-solution[j])*graph[i,j]
            
    return res
    
def random_solution(n):
    return random.sample([0]*(n//2)+[1]*(n//2),n-(n%2))        

if __name__=="__main__":
    filepath = sys.argv[1]
    g = parser(filepath)
    
    for i in range(10):
        rs = random_solution(len(g))
        print(str(rs) + " -> " + str(objective_function(g,rs)))
        
    