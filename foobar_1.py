# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 09:36:37 2021

@author: h12962
"""
def solution(s):
    # braille dictionary
    braille_dict = {'a':'100000',
                    'b':'110000',
                    'c':'100100',
                    'd':'100110',
                    'e':'100010',
                    'f':'110100',
                    'g':'110110',
                    'h':'110010',
                    'i':'010100',
                    'j':'010110',
                    'k':'101000',
                    'l':'111000',
                    'm':'101100',
                    'n':'101110',
                    'o':'101010',
                    'p':'111100',
                    'q':'111110',
                    'r':'111010',
                    's':'011100',
                    't':'011110',
                    'u':'101001',
                    'v':'111001',
                    'w':'010111',
                    'x':'101101',
                    'y':'101111',
                    'z':'101011',
                    '$':'000001', #single charactor value for capitalization mark
                    ' ':'000000'}

    for letter in s:
        if letter.isupper() == True:
            letter_cap = str(braille_dict['$'])+str(braille_dict[letter.lower()])
            s = s.replace(letter, letter_cap)
        
        else:
            s = s.replace(letter, braille_dict[letter])
    
    print(s)