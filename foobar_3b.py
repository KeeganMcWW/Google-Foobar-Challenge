'''
from itertools import combinations, chain
from operator import sub

def solution(x):
    sum_combinations = []
    count = 0
    # the following function is taken for this stackoverflow solution
    # https://stackoverflow.com/questions/2065553/get-all-numbers-that-add-up-to-a-number/2074693

    # it generates the possible combinations of lists with sum to some n
    def sum_to_n(n):
        """generate the series of +ve integer lists which sum to a +ve integer, n."""
        b, mid, e = [0], list(range(1, n)), [n]
        splits = (d for i in range(n) for d in combinations(mid, i))
        return (list(map(sub, chain(s, e), chain(b, s))) for s in splits)
    # now filter them by a set of logical rules which make up a staircase
    for combination in sum_to_n(x):
        # if it is in ascending order (you can't have more higher steps than lower steps...)
        # if the staircase is not height 1
        # if they are not all the same value (this would be more of a plateau than a stair case)
        # and if there are repeats of neighboring values (which would create step too low to climb)
        if list(reversed(sorted(combination))) == combination \
                and len(combination) != 1 \
                and not all(elem == combination[0] for elem in combination) \
                and all(elem != combination[index-1] and elem != combination[index+1]
                        for index, elem in enumerate(combination[:-1])):
            #sum_combinations.append(combination)
            count = count + 1
        else:
            pass
    if x == 2:
        #sum_combinations = [[1,1]]
        count = count + 1
    return count
'''

'''
def solution_2(x):
    # code source can be found at the following website
    # https://www.geeksforgeeks.org/find-all-combinations-that-adds-upto-given-number-2/
    # arr - array to store the combination
    # index - next location in array
    # num - given number
    # reducedNum - reduced numberg
    count = 0
    def findCombinationsUtil(arr, index, num,
                             reduced_num, lst, count):
        temp_combination = []
        # Base condition
        if reduced_num < 0:
            return
        if reduced_num == 0:
            for i in range(index):
                temp_combination.append(arr[i])
            if list(sorted(temp_combination)) == temp_combination \
                    and len(temp_combination) != 1 \
                    and not all(elem == temp_combination[0] for elem in temp_combination) \
                    and all(elem != temp_combination[index - 1] and elem != temp_combination[index + 1]
                            for index, elem in enumerate(temp_combination[:-1])):
                lst.append(temp_combination)
            return
        # Find the previous number stored in arr[].
        # It helps in maintaining increasing order
        prev = 1 if (index == 0) else arr[index - 1]
        # note loop starts from previous
        # number i.e. at array location
        # index - 1
        for k in range(prev, num + 1):
            # next element of array is k
            arr[index] = k
            # call recursively with
            # reduced number
            findCombinationsUtil(arr, index + 1, num,
                                 reduced_num - k, lst, count + 1)
        return lst, count
    # Function to find out all
    # combinations of positive numbers
    # that add upto given number.
    # It uses findCombinationsUtil()
    arr = [0] * n
    lst = []
    # find all combinations
    return findCombinationsUtil(arr, 0, x, x, lst, count)
'''
import math
def solution(x):
    # I got totally lost and hung up on a different solution which did not work in a reasonable time frame. I used the
    # following explanation on reddit and followed along, I will annotate the code for my own better understanding .
    # https://www.reddit.com/r/learnprogramming/comments/5vysej/google_foobar_level_3_help/de6uesn/
    # the following formula is the one that applies to this problem
    # Q(n, k) = Q(n-k, k) + Q(n-k, k-1) for n>k>=1, with Q(1, 1)=1, Q(n, 0)=0 (n>=1).
    # the mathematics are described here
    # https://en.wikipedia.org/wiki/Partition_(number_theory)#Odd_parts_and_distinct_parts
    max_memo = int(math.floor(((8 * x + 1) ** .5 - 1) / 2))
    # a memo is generated to log the recursive functions solution, in this case we are just making a big matrix
    memo = [[None for k in range(max_memo + 1)] for n in range(x + 1)]
    def Q(n,k):
        # initial cases
        if n and k == 1:
            return 1
        if n > 0 and k == 0:
            return 0
        if n < k or k < 1:
            return 0
        # if the memos entry is black, perform the operation and return the memo entry back out
        if memo[n][k] is None:
            memo[n][k] = Q(n-k,k) + Q(n-k,k-1)
        return memo[n][k]
    max_k = int(math.floor(((8 * n + 1) ** .5 - 1) / 2))
    print(sum(Q(n, k) for k in range(max_k + 1)) - 1)
# Driver code
(solution(3))
(solution(4))
(solution(5))
(solution(6))
(solution(7))
(solution(8))
(solution(9))
(solution(10))
(solution(200))

