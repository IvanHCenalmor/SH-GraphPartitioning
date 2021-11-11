#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 16:40:44 2021

@author: cocomputer
"""

import random
import numpy as np

with open("Cebe.bip.n10.1", "r") as f:
    n = int(f.readline())
    m = [[int(i) for i in line.split('   ')[:-1]] for line in f.readlines()]
    
nums = np.array([random.sample([0]*(n//2)+[1]*(n//2), n)])

A = (1 - nums) * nums.transpose()

W = A + A.transpose()

solution = np.sum(m*W)//2