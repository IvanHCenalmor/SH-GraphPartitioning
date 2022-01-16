#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:54:14 2021

@author: cocomputer
"""

import gp_util as util
import gp_local_search as ls
import gp_population as pop

import numpy as np
import time
import itertools

datasets = ['Cebe.bip.n10.1','Cebe.bip.n10.2','Cebe.bip.n10.3','Cebe.bip.n10.4', 'Cebe.bip.n10.5',
            'Cebe.bip.n20.1','Cebe.bip.n20.2','Cebe.bip.n20.3','Cebe.bip.n20.4', 'Cebe.bip.n20.5',
            'G.sub.500', 'G124.02', 'G124.16', 'G250.02', 'G250.04', 'G250.08', 'G500.04', 'G500.005',
            'G1000.02', 'G1000.005', 'G1000.0025']

datasets2 = ['Cebe.bip.n10.1','Cebe.bip.n10.2','Cebe.bip.n10.3','Cebe.bip.n10.4', 'Cebe.bip.n10.5',
            'Cebe.bip.n20.1','Cebe.bip.n20.2','Cebe.bip.n20.3','Cebe.bip.n20.4', 'Cebe.bip.n20.5']
        
def brute_force():
    for g_str in datasets2:
        n, graph = util.parser(g_str)
        
        best_sol = [True]*(n//2)+[False]*(n//2)
        best_cost = util.objective_function(graph, best_sol)
        
        
        for positions in itertools.combinations(range(1,n),n//2-1):
            p = [1] + [0]*(n-1)
            
            for i in positions:
                p[i] = 1
                
            cost = util.objective_function(graph,p)
            if cost < best_cost:
                best_sol = p
                best_cost = cost
        
    
        print(g_str)
        print('Best solution: {}'.format(best_sol))
        print('Best cost: {}'.format(best_cost))
        print()

def aco_test(g):
    
    normalized_graph = g/np.amax(g)
    
    n = min(len(g), 100)
    generations = util.max_evals//n
    
    best_sol, _ = pop.ant_colony_opt(normalized_graph, generations=generations, k_best=n//5, 
                                     population_size=n, dissipation_factor=0.05, 
                                     beta=3/4, e = 0.1, min_pheromone = 0.05, max_pheromone = 1)
    
    best_cost = util.objective_function(g, best_sol)
    
    return best_cost    

def ms_test(g):    
    best_sol, best_cost = ls.multistart(g, 100000)
    
    #print('Best solution: {}'.format(best_sol))
    #print('Best cost: {}'.format(best_cost))
    
    #print('Counter: {}'.format(util.evals))
    
    return best_cost

def gr_test(g):
    best_sol, best_cost = ls.grasp(g, len(g)//5, 100000)
    
    #print('Best solution: {}'.format(new_solution))
    #print('Best cost: {}'.format(new_cost))
    
    #print('Counter: {}'.format(util.evals))
    
    return best_cost

def sa_test(g,temp):
    alpha = 0.99
    chain_max = 1
    reject_max = 5*len(g)
    
    best_sol, best_cost = ls.simulated_annealing(g,temp,alpha,chain_max,reject_max)

    #print('Best solution: {}'.format(new_solution))
    #print('Best cost: {}'.format(new_cost))
    
    #print('Counter: {}'.format(util.evals))
    
    return best_cost

def tests():            
    for g_str in datasets:
        n, graph = util.parser(g_str)
        
        temp = ls.temperature_estimator(graph)
        util.evals = 0
    
        costs = []
        evals = []
        times = []
        
        for _ in range(10):
            init_time = time.time()
            costs.append(sa_test(graph,temp))
            times.append(time.time()-init_time)
            evals.append(util.evals)
            util.evals = 0
        
        results = np.array((costs,evals,times))
        np.save("tests/simulated_annealing/evals10k/{}.npy".format(g_str),results)   
            
def load():
    x = np.load("tests/ant_colony_optimization/evals10k/{}.npy".format('G1000.0025'))
    x = np.array(x,dtype="int")
    print(x)

if __name__=="__main__":
    tests()