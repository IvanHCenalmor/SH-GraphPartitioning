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
            'G.sub.500', 'G124.02', 'G124.16', 'G250.02', 'G250.04', 'G250.08', 'G500.04', 'G500.05',
            'G1000.02', 'G1000.005', 'G1000.0025']

def main6():
    for d in datasets:
        n, graph = util.parser(d)
        #n, graph = util.parser('Cebe.bip.n10.1')
        init_time = time.time()
        best_sol, best_cost = pop.ant_colony_opt(graph, generations=100, k_best=n//2, population_size=int(n*0.75), dissipation_factor=0.02, 
                                                 alpha=0.5, e = 0.1, min_pheromone = 0.1, max_pheromone = 1)
        print('---{}---'.format(d))
        print('Time: {}'.format(time.time() - init_time))
        print('Best solution: {}'.format(best_sol))
        print('Best cost: {}'.format(best_cost))
        print()

def main5():
    n, graph = util.parser('G124.02')
    
    init_time = time.time()
    best_sol, best_cost = pop.ant_colony_opt(graph, generations=100, k_best=n//2, dissipation_factor=0.02, 
                                             alpha=0.5, e = 0.1, min_pheromone = 0.1, max_pheromone = 1)
    print('Time: {}'.format(time.time() - init_time))
        
    
def main4():
    n, graph = util.parser('Cebe.bip.n10.2')
    
    best_sol = [True]*(n//2)+[False]*(n//2)
    best_cost = util.objective_function(graph, best_sol)
    
    permutations = itertools.permutations(best_sol)
    
    for p in permutations:
        cost = util.objective_function(graph,p)
        if cost < best_cost:
            best_sol = p
            best_cost = cost

    print('Best solution: {}'.format(best_sol))
    print('Best cost: {}'.format(best_cost))

def main3():
    n, graph = util.parser('Cebe.bip.n10.1')
    
    best_sol, best_cost = ls.multistart(graph, 50)
    
    print('Best solution: {}'.format(best_sol))
    print('Best cost: {}'.format(best_cost))
    
    print('Counter: {}'.format(util.evals))

def main2():
    n, graph = util.parser('Cebe.bip.n10.1')
    
    new_solution, new_cost = ls.grasp(graph, 3, 50)
    
    print('Best solution: {}'.format(new_solution))
    print('Best cost: {}'.format(new_cost))
    
    print('Counter: {}'.format(util.evals))

def main():
    n, graph = util.parser('Cebe.bip.n10.1')
    
    temp = ls.temperature_estimator(graph)
    
    util.evals = 0
    
    alpha = 0.99
    chain_max = 1
    reject_max = 50
    
    new_solution, new_cost = ls.simulated_annealing(graph,temp,alpha,chain_max,reject_max)

    print('Best solution: {}'.format(new_solution))
    print('Best cost: {}'.format(new_cost))
    
    print('Counter: {}'.format(util.evals))            
    

if __name__=="__main__":
    main6()