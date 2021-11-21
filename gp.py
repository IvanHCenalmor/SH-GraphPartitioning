#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:54:14 2021

@author: cocomputer
"""

import gp_util as util
import gp_local_search as ls

import numpy as np

import itertools

def main3():
    n, graph = util.parser('Cebe.bip.n10.1')
    
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

def main2():
    n, graph = util.parser('Cebe.bip.n10.1')
    
    solution = util.greedy_solution(n, graph)
    
    new_solution, new_cost = ls.local_search(graph,solution)
    
    print(new_solution)
    print(new_cost)

def main():
    n, graph = util.parser('Cebe.bip.n10.1')
    
    temp = ls.temperature_estimator(graph)
    alpha = 0.99
    chain_max = 1
    reject_max = 50
    
    new_solution, new_cost = ls.simulated_annealing(graph,temp,alpha,chain_max,reject_max)
        
    print(util.objective_function(graph, new_solution))
    print(new_cost)

if __name__=="__main__":
    main()