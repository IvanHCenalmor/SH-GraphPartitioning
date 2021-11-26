#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 11:06:33 2021

@author: cocomputer
"""

import gp_util as util
import numpy as np 
import math

def ant_colony_opt(graph, population, generations, k_best, dissipation_factor):
    n = len(graph)
    
    pheromones = np.ones((2,n))
    
    best_sol = None
    best_cost = math.inf
    
    for i in range(generations):
        pop = [ant_solution( graph, pheromones) for _ in range(population)]
        costs = [util.objective_function(graph, solution) for solution in pop] 
            
        sorted_factors = sorted(zip(pop, costs), key=lambda x:x[1], reverse=True)
        sorted_factors = sorted_factors[:k_best]
        k_pop, k_costs = zip(*sorted_factors)
        
        if k_costs[0] < best_cost:
            best_sol = k_pop[0]
            best_cost = k_costs[0]
            
        pheromones *= (1 - dissipation_factor)
        pheromones += increment_pheromone(k_pop, k_costs, n)    
            
    return best_sol, best_cost


def ant_solution(graph, pheromones, initial_vertex, alpha, e = 0.1):
    solution = [initial_vertex]
    cost = 0
    
    dist_p0 = graph[initial_vertex] + e
    dist_p1 = np.zeros(len(graph)) + e
    
    not_visited = np.ones(len(graph),dtype=bool)
    not_visited[initial_vertex] = False
    
    for i in range(1,len(graph)):
        verts = np.array(range(len(graph)))[not_visited]
        f0 = dist_p0[not_visited]
        f1 = dist_p1[not_visited]
        phe = graph[solution[-1]][not_visited]
        
        prob = phe**alpha * (f1/f0 if i&1 else f0/f1)
        prob = prob/sum(prob)
        
        vertex = np.random.choice(verts,size=1,p=prob)
        not_visited[vertex] = False
        solution.append(vertex)
        
        if i&1: dist_p1 += graph[vertex]
        else: dist_p0 += graph[vertex]
        
        cost += graph[solution[-1]][vertex]
           
    return solution, cost


def increment_pheromone(solutions, costs, n):
    
    increment = np.zeros((2,n))
    
    # Multiplicar solution por 1/cost y sumar a segunda fila increment
    # Multiplicar ¬solution por 1/cost y sumar a primera fila increment
    
    return increment