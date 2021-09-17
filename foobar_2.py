# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 10:44:24 2021

@author: h12962
"""

def solution(s):
    # here I am going to change the reference frame to that of the bunnies moving right
    def step_left(hallway_string):
        #bunny walks away
        if hallway_string[0] == '<':
            hallway_list = list(hallway_string)    
            hallway_list[0] = '-'
            hallway_string = ''.join(hallway_list)
        #find all bunnies in hallway    
        left_faced_index= find(hallway_string,'<')
        #move the bunnies left
        new_hallway_string = hallway_string
        for position in left_faced_index:
            new_hallway_string = swap(new_hallway_string,position, position-1)
    
        return(new_hallway_string)
    
    def step_right(hallway_string):
        #bunny walks away
        if hallway_string[-1] == '>':
            hallway_list = list(hallway_string)    
            hallway_list[-1] = '-'
            hallway_string = ''.join(hallway_list)
        #find all bunnies in hallway    
        left_faced_index= find(hallway_string,'>')
        #move the bunnies left
        new_hallway_string = hallway_string
        for position in left_faced_index:
            new_hallway_string = swap(new_hallway_string,position, position+1)
    
        return(new_hallway_string)        
    def find(lst, a):
        result = []
        for i, x in enumerate(lst):
            if x==a:
                result.append(i)
        return result
    
    def swap(string, a, b):
        lst = list(string)
        lst[a], lst[b] = lst[b], lst[a]
        return ''.join(lst)
    
    def salute_counter(string):
        return string.count('><') *2
    
    #inital number of salutes
    salutes = salute_counter(s)
    #step and check
    for left_bun in range(len(s)):
        stepped_s = step_right(s)
        count = salute_counter(stepped_s)
        salutes = salutes + count
        s = stepped_s
    
    return salutes
    
    
    