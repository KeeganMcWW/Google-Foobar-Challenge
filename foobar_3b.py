from itertools import combinations, chain
def solution(x):  
    staircase = []    
    def sum_to_n(n):
        'Generate the series of +ve integer lists which sum to a +ve integer, n.'
        from operator import sub
        b, mid, e = [0], list(range(1, n)), [n]
        splits = (d for i in range(n) for d in combinations(mid, i)) 
        return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)
            
    return 