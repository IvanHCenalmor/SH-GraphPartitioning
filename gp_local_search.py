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

def local_search(graph, solution):
    
    cost = util.objective_function(graph,solution)
    part0 = np.where(~solution)[0]
    part1 = np.where(solution)[0]
    
    e = util.evals
    
    new_solution, new_cost = util.improved_random_neighbor(graph,solution,part0,part1,cost)
    
    while new_solution.size!=0 and util.evals<=util.max_evals:
        solution, cost = new_solution, new_cost
        new_solution, new_cost = util.improved_random_neighbor(graph,solution,part0,part1,cost)
        
    return solution, cost

def multistart(graph, n_times):
    
    init_solution = util.random_solution(len(graph))
    best_solution, best_cost = local_search(graph,init_solution)
    
    for _ in range(n_times-1):
        if util.evals>util.max_evals:
            break
        init_solution = util.random_solution(len(graph))
        solution, cost = local_search(graph,init_solution)
        if cost < best_cost:
            best_solution = solution
            best_cost = cost
        
    return best_solution, best_cost

def grasp(graph, k, n_times):
    
    init_solution = util.constructive_method(graph, k)
    best_solution, best_cost = local_search(graph,init_solution)
    
    for _ in range(n_times-1):
        if util.evals>util.max_evals:
            break
        init_solution = util.constructive_method(graph, k)
        solution, cost = local_search(graph,init_solution)
        if cost < best_cost:
            best_solution = solution
            best_cost = cost
        
    return best_solution, best_cost
    
    
def simulated_annealing(graph,temp,alpha,chain_max,reject_max):
    reject_size = 0
    
    solution = util.random_solution(len(graph))
    cost = util.objective_function(graph,solution)
    part0 = np.where(~solution)[0]
    part1 = np.where(solution)[0]
    
    best_solution, best_cost = solution, cost
    
    while reject_size<reject_max and util.evals<=util.max_evals:
        chain_size = 0
        
        while chain_size<chain_max and reject_size<reject_max:
            new_solution, new_cost, i0, i1 = util.random_neighbor(graph,solution,part0,part1,cost)
            delta = new_cost-cost
            '''
            print("\n")
            print("Current solution: {}".format(solution))
            print("Objective function: {}".format(cost))
            print("Proposed solution: {}".format(new_solution))
            print("Proposed objective function: {}".format(new_cost))
            print("c: {}".format(temp))
            '''
            if delta<0 or math.exp(-1*delta/temp)>random.random():
                part0[i0], part1[i1] = part1[i1], part0[i0]
                reject_size = 0
                solution = new_solution
                cost = new_cost
                #print("Accepted")
                if cost < best_cost:
                    best_solution = solution
                    best_cost = cost
            
            else: 
                reject_size += 1
                #print("Rejected")
            
            chain_size += 1
        
        temp *= alpha
        
    return best_solution, best_cost
                
def temperature_estimator(graph, sample_size = 10000, accept_rate = 0.5):
    deltas = []
    
    while len(deltas)<sample_size:
        solution = util.random_solution(len(graph))
        cost = util.objective_function(graph,solution)
        part0 = np.where(~solution)[0]
        part1 = np.where(solution)[0]
        
        _, new_cost, _, _ = util.random_neighbor(graph,solution,part0,part1,cost)
        
        delta = new_cost-cost
        
        deltas.append(abs(delta))
            
    return -1*sum(deltas)/len(deltas)/math.log(accept_rate)