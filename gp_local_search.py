#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 17:19:15 2021

@author: manu
"""

import gp_util
import random
import math
import numpy as np


def simulated_annealing(graph,solution,temp,alpha,chain_max,reject_max):
    reject_size = 0
    cost = gp_util.objective_function(graph,solution)
    part1 = np.where(solution)[0]
    part2 = np.where(not solution)[0]
    
    while reject_size<reject_max:
        chain_size = 0
        
        while chain_size<chain_max and reject_size<reject_max:
            new_solution, new_cost = gp_util.random_neighbor_swap(graph,solution,part1,part2,cost)
            delta = new_cost-cost
            
            if delta<0 or math.exp(-1*delta/temp)>random.random():
                reject_size = 0
                solution = new_solution
                cost = new_cost
            
            else: reject_size += 1
            
            chain_size += 1
        
        temp *= alpha
        
    return solution, cost
                
    
