#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:06:33 2021

@author: cocomputer
"""

from multiprocessing import Process, Queue
import numpy as np 
import math

import gp_util as util

def ant_colony_opt(graph, generations, k_best, dissipation_factor, 
                   alpha, e = 0.1, min_pheromone = 0, max_pheromone = 1):
    
    n = len(graph)
    
    pheromones = np.ones((n,n))*(max_pheromone - min_pheromone)
    
    min_phe_matrix = np.ones((n,n))*min_pheromone
    max_phe_matrix = np.ones((n,n))*max_pheromone
    
    best_sol = None
    best_cost = math.inf
    
    q = Queue()
    for i in range(generations):
        
        for i in range(n):
            p = Process(target=ant_solution_queue, args=(graph, pheromones, i, alpha, q, e,))
            p.start()
            
        pop_costs=np.empty(n,dtype='object')
        for i in range(n):
            pop_costs[i] = q.get()
        
        #pop_costs = [ant_solution(graph, pheromones, i, alpha, e) for i in range(n)]
        
        sorted_pop = sorted(pop_costs, key=lambda x:x[1])
        sorted_pop = sorted_pop[:k_best]
        k_pop, k_costs = zip(*sorted_pop)
        if k_costs[0] == 0:
            return k_pop[0], k_costs[0]
        if k_costs[0] < best_cost:
            best_sol = k_pop[0]
            best_cost = k_costs[0]
        
        pheromones = np.maximum(min_phe_matrix, pheromones*(1 - dissipation_factor))
        pheromones = np.minimum(max_phe_matrix, pheromones+increment_pheromone(k_pop, k_costs, n)) 
        
    return best_sol, best_cost

def ant_solution_queue(graph, pheromones, initial_vertex, alpha, q, e = 0.1):
    q.put(ant_solution(graph, pheromones, initial_vertex, alpha, e))

def ant_solution(graph, pheromones, initial_vertex, alpha, e = 0.1):
    solution = [initial_vertex]
    bool_solution = np.zeros(len(graph), dtype=bool)
    
    dist_p0 = graph[initial_vertex] + e
    dist_p1 = np.zeros(len(graph)) + e
    
    not_visited = np.ones(len(graph),dtype=bool)
    not_visited[initial_vertex] = False
    
    for i in range(1,len(graph)):
        verts = np.array(range(len(graph)))[not_visited]
        f0 = dist_p0[not_visited]
        f1 = dist_p1[not_visited]
        phe = pheromones[solution[-1]][not_visited]
        
        prob = phe**alpha * (f1/f0 if i&1 else f0/f1)
        prob = prob/sum(prob)
        
        vertex = np.random.choice(verts,size=1,p=prob)[0]

        not_visited[vertex] = False
        solution.append(vertex)
        
        if i&1: 
            dist_p1 += graph[vertex]
            bool_solution[vertex] = True
        else: 
            dist_p0 += graph[vertex]
     
    cost = util.objective_function(graph, bool_solution)
           
    return solution, cost

def increment_pheromone(solutions, costs, n):
    
    increment = np.zeros((n,n))

    for sol,c in zip(solutions,costs):
        for i in range(len(sol)-1):
            increment[sol[i],sol[i+1]] += 1/c
        increment[sol[0], sol[-1]] += 1/c
        
    increment += increment.transpose()
    
    return increment

def permutation_to_solution(permutation):
    even_indx = np.array([b for i,b in enumerate(permutation) if i&1])
    sol = np.ones((len(permutation)), dtype=bool)
    sol[even_indx] = False
    return sol