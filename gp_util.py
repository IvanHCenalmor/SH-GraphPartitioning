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


def neighbour(graph, solution, v0, v1, cost):
    new_solution = np.copy(solution)
    new_solution[v0] = True
    new_solution[v1] = False
    
    inv_new_solution = ~new_solution
    
    new_cost = cost + np.dot(graph[v0],inv_new_solution) - np.dot(graph[v0],new_solution) 
    new_cost += np.dot(graph[v1],new_solution) - np.dot(graph[v1],inv_new_solution) 
    new_cost -= 2*graph[v0][v1]
    
    return new_solution, new_cost

def random_neighbor(graph, solution, part0, part1, cost):
    i0 = random.randrange(len(part0))
    i1 = random.randrange(len(part1))
    
    new_solution, new_cost = neighbour(graph,solution,part0[i0],part1[i1],cost)
    
    return new_solution, new_cost, i0, i1
    
def improved_random_neighbor(graph, solution, part0, part1, cost):
    rindxs0 = list(range(len(part0)))
    rindxs1 = list(range(len(part1)))   
    
    random.shuffle(rindxs0)
    random.shuffle(rindxs1)
    
    for i0 in rindxs0:
        for i1 in rindxs1:
            new_solution, new_cost = neighbour(graph,solution,part0[i0],part1[i1],cost)
            
            if new_cost<cost:
                part0[i0], part1[i1] = part1[i1], part0[i0]
                return new_solution, new_cost
            
    return np.array([]), 0