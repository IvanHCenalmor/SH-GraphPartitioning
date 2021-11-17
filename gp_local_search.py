#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 17:19:15 2021

@author: manu
"""

import gp_util as util
import random
import math
import numpy as np

import time

def simulated_annealing(graph,solution,temp,alpha,chain_max,reject_max):
    reject_size = 0
    cost = util.objective_function(graph,solution)
    part1 = np.where(solution)[0]
    part2 = np.where(~solution)[0]
    
    while reject_size<reject_max:
        chain_size = 0
        
        while chain_size<chain_max and reject_size<reject_max:
            new_solution, new_cost, i1, i2 = util.random_neighbor_swap(graph,solution,part1,part2,cost)
            delta = new_cost-cost
            
            print("\n")
            print("Current solution: {}".format(solution))
            print("Objective function: {}".format(cost))
            print(" Proposed solution: {}".format(new_solution))
            print("Proposed objective function: {}".format(new_cost))
            print("c: {}".format(temp))
            
            if delta<0 or math.exp(-1*delta/temp)>random.random():
                part1[i1], part2[i2] = part2[i2], part1[i1]
                reject_size = 0
                solution = new_solution
                cost = new_cost
                print("Accepted")
            
            else: 
                reject_size += 1
                print("Rejected")
            
            chain_size += 1
        
        temp *= alpha
        
    return solution, cost
                
def mean_delta(graph):
    deltas = []
    
    for i in range(100):
        rs = util.random_solution(len(graph))
        part1 = np.where(rs)[0]
        part2 = np.where(~rs)[0]
        cost = util.objective_function(graph,rs)
        
        for j in range(100):
            _, rc, _, _ = util.random_neighbor_swap(graph, rs, part1, part2, cost)
            delta = rc - cost
            
            if delta>0: deltas.append(delta)
            
    return sum(deltas)/len(deltas)