#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:29:25 2021

@author: manu
"""
import numpy as np
import random

evals = 0
max_evals = 10000

class pair(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __hash__(self):
        return (self.x+self.y)*(self.x+self.y+1)//2+self.y

def parser(filepath):
    with open("data/{}".format(filepath), "r") as f:
        if filepath[0] == 'C':
                n = int(f.readline())
                m = [[int(i) for i in line.split('   ')[:-1]] for line in f.readlines()]
        else:
                first_line = f.readline()[:-1].split(' ')
                n = int(first_line[0])
                m = np.zeros((n,n))
                for i,line in enumerate(f.readlines()):
                    for j in line[:-1].split(' '):
                        if(j):
                            m[i,int(j)-1] += 1
                    
    return n, np.array(m)
                

def objective_function(graph, solution):
    global evals
    evals += 1
    
    aux_sol = np.array([solution])
    
    A = (1 - aux_sol)*aux_sol.transpose()

    W = A + A.transpose()
    
    return np.sum(graph*W)/2    
    
def objective_function2(graph, solution):
    global evals
    evals += 1
    
    res = 0
    
    for i in range(0,len(graph)-1):
        for j in range(i+1,len(graph)):
            res += abs(solution[i]-int(solution[j]))*graph[i][j]
            
    return res

def random_solution(n):
    return np.array(random.sample([True]*(n//2)+[False]*(n//2),n),dtype="bool8")

def constructive_method(graph, k, e=0.01):
    n = len(graph)
    
    possible_nodes = list(range(n))
    not_used = np.ones(n, dtype=bool)
    solution = np.zeros(n, dtype=bool)
    
    first_indx = random.randint(0, n-1)
    first_node = possible_nodes.pop(first_indx)
    
    not_used[first_node] = False
    solution[first_node] = True
    
    dist_p1 = graph[first_node] + e
    dist_p2 = np.zeros(n) + e
    
    factors = dist_p2[not_used]/dist_p1[not_used]
    
    for i in range(n-2):
        sorted_factors = sorted(enumerate(factors), key=lambda x:x[1], reverse=True)
        sorted_factors = sorted_factors[:min(k,len(sorted_factors))]
        f_indx, f = zip(*sorted_factors)
        
        prob = f / np.sum(f)
        node_indx = np.random.choice(f_indx, 1, p=prob)[0]
        node = possible_nodes.pop(node_indx)
        
        if i % 2 == 0:  
            not_used[node] = False
            
            dist_p2 += graph[node]
            factors = dist_p1[not_used]/dist_p2[not_used]
        else:
            not_used[node] = False
            solution[node] = True
            
            dist_p1 += graph[node]
            factors = dist_p2[not_used]/dist_p1[not_used]

    return solution

def neighbour(graph, solution, v0, v1, cost):
    global evals
    evals += 1
    
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
            
            elif evals>max_evals: break
        
        if evals>max_evals: break
            
    return np.array([]), 0
