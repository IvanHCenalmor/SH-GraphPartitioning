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
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __hash__(self):
        return (self.x+self.y)*(self.x+self.y+1)//2+self.y

def parser(filepath):
    with open(filepath, "r") as f:
        n = int(f.readline())
        m = [[int(i) for i in line.split('   ')[:-1]] for line in f.readlines()]
        return n, np.array(m)

def objective_function(graph, solution):
    
    aux_sol = np.array([solution])
    
    A = (1 - aux_sol)*aux_sol.transpose()

    W = A + A.transpose()
    
    return np.sum(graph*W)/2    
    
def objective_function2(graph, solution):
    res = 0
    
    for i in range(0,len(graph)-1):
        for j in range(i+1,len(graph)):
            res += abs(solution[i]-int(solution[j]))*graph[i][j]
            
    return res

def random_solution(n):
    return np.array(random.sample([True]*(n//2)+[False]*(n//2),n),dtype="bool8") 

def random_neighbor_swap(graph, solution, part1, part2, cost):
    
    indx1 = random.randrange(len(part1))
    i = part1[indx1]
    indx2 = random.randrange(len(part2))
    j = part2[indx2]
    
    part1[indx1] = j
    part2[indx2] = i
    
    new_solution = np.copy(solution)
    new_solution[i] = False
    new_solution[j] = True
    
    inv_new_solution = ~new_solution
    
    new_cost = cost + np.dot(graph[i],new_solution) - np.dot(graph[i],inv_new_solution) 
    new_cost += np.dot(graph[j],inv_new_solution) - np.dot(graph[j],new_solution) 
    new_cost -= 2*graph[i][j] 
    
    return new_solution, new_cost
    

def main():
    
    n, graph = parser('Cebe.bip.n10.1')
    
    solution = random_solution(n) 
    
    cost = objective_function(graph, solution)
    
    part1 = np.where(solution)[0]
    part2 = np.where(~solution)[0]
        
    for i in range(100):
        
        solution, cost = random_neighbor_swap(graph, solution, part1, part2, cost)
        
        print()
        #print(objective_function(graph, solution))
        #print(cost)
        print(part1)
        print(part2)

if __name__=="__main__":
    main()