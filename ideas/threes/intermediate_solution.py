# Proof of concept solution for intermediate part of:
# https://www.reddit.com/r/dailyprogrammer_ideas/comments/3nvleu/easyintermediatehard_a_game_of_threes/

import sys, time
from functools import lru_cache
from math import log, ceil, floor
from queue import PriorityQueue

class AddChainValue(object):
    def __init__(self, current, prev_value, prev_move):
        self.current = current
        self.prev_value = prev_value
        self.prev_move = prev_move

        if prev_value:
            self.score = prev_value.score + (0 if prev_move else 1) # increase score when the move was a 0
        else:
            self.score = 0

    def __lt__(self, value):
        return self.score < value.score

    def get_valid_moves(self):
        if self.current % 3 == 0:
            return (0,)
        elif self.current == 2:
            return (1,)
        elif self.current % 3 == 1:
            return (-1, 2)
        else:
            return (-2, 1)

    def do_next_move(self, next_move):
        assert next_move in self.get_valid_moves()
        
        next_value = (self.current + next_move) // 3
        return AddChainValue(next_value, self, next_move)

    @lru_cache(maxsize=65536)
    def get_multiple3_distance(num):
        max_exp = floor(log(num, 3))
        distance = 1
        zeroes = 0
        for exp in range(2, max_exp+1): # Look for closest multiples of 9 .. 2^maxpow, selfish
            power = 3 ** exp
            multiple_low = (num // power) * power
            multiple_high = multiple_low + power
            min_delta = min(num - multiple_low, multiple_high - num)
            if min_delta == 0:
                zeroes += 1
            elif min_delta < distance:
                distance = min_delta
        distance = distance / (zeroes + 1)
        return distance

    def get_priority(self, next_move):
        ''' XXX: This is a crapshoot. What am I even doing. '''
        return 1
        assert next_move in self.get_valid_moves()
        #if next_move == 0:
        #    return 0

        next_value = self.current + next_move
        if next_value == 1:
            return 0

        best_priority = AddChainValue.get_multiple3_distance(next_value)

        return best_priority * self.score

    def display(self, move_to_display):
        if self.prev_value:
            self.prev_value.display(self.prev_move)
        if move_to_display is not None:
            print("%s %s" % (self.current, move_to_display))
        else:
            print(self.current)
        

if len(sys.argv) > 1:
    N  = int(sys.argv[1])
else:
    N = int(input("N? "))


start_chain = AddChainValue(N, None, None)
chain_queue.put( (0, start_chain) )

known_best_scores = {}
best_solution = None

tick = time.time()

while not chain_queue.empty():
    _, chain = chain_queue.get()
    if chain.current == 1:
        print(chain.score)
        if (not best_solution) or (best_solution.score < chain.score):
            best_solution = chain
        continue

    if time.time() - tick > 1:
        print("... Queue size: %s; Current: %s" % (chain_queue.qsize(), chain.current))
        tick = time.time()

    if chain.current not in known_best_scores:
        known_best_scores[chain.current] = chain.score
    else:
        if known_best_scores[chain.current] < chain.score:
            known_best_scores[chain.current] = chain.score
        else:
            continue

    next_moves = chain.get_valid_moves()
    for move in next_moves:
        p = chain.get_priority(move)
        next_chain = chain.do_next_move(move)
        chain_queue.put( (p, next_chain) )
        

if best_solution:
    best_solution.display(None)
    print(best_solution.score)
else:
    print("Impossible.")
    
