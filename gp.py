#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 15:54:14 2021

@author: cocomputer
"""

import  gp_util as util
import gp_local_search as ls

import numpy as np

def main():
    
    n, graph = util.parser('Cebe.bip.n10.1')
    
    solution = util.random_solution(n) 
    
    temp = 0.5
    alpha = 0.99
    chain_max = 1
    reject_max = 10
    
    new_solution, new_cost = ls.simulated_annealing(graph,solution,temp,alpha,chain_max,reject_max)
        
    print(util.objective_function(graph, new_solution))
    print(new_cost)

if __name__=="__main__":
    main()