# Proof of concept solution for intermediate part of:
# https://www.reddit.com/r/dailyprogrammer_ideas/comments/3nvleu/easyintermediatehard_a_game_of_threes/

import sys
from math import log, ceil, floor
from queue import PriorityQueue

class AddChain(object):
    def __init__(self, start, moves=[]):
        self.start = start
        self.moves = moves[:]

        self.current = self.start
        self.score = 0
        for m in self.moves:
            self.current = (self.current + m) // 3
            self.score += 1 if m else 0

    def __lt__(self, chain):
        return self.score < chain.score

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
        
        return AddChain(self.start, self.moves + [next_move])

    def get_priority(self, next_move):
        ''' XXX: This is a crapshoot. What am I even doing. '''
        assert next_move in self.get_valid_moves()
        if next_move == 0:
            return 0

        next_value = self.current + next_move
        if next_value == 1:
            return 0

        if next_move > 1:  # Moving up, check distance to next highest power of 3
            next_power = ceil(log(next_value))
        else:
            next_power = floor(log(next_value))
        
        delta = abs(log(next_value) - next_power) # 0.0 .. 1.0

        priority = delta * self.score # weight it by how much we've scored so far
        return priority

    def display(self):
        x = self.start
        for m in self.moves:
            print("%s %s" % (x, m))
            x = (x + m) // 3
        print(self.current)
        

if len(sys.argv) > 1:
    N  = int(sys.argv[1])
else:
    N = int(input("N? "))

chain_queue = PriorityQueue()

start_chain = AddChain(N, [])
chain_queue.put( (0, start_chain) )

while not chain_queue.empty():
    _, chain = chain_queue.get()
    if chain.current == 1:
        chain.display()
        break

    next_moves = chain.get_valid_moves()
    for move in next_moves:
        p = chain.get_priority(move)
        next_chain = chain.do_next_move(move)
        chain_queue.put( (p, next_chain) )
        
else:
    print("Impossible.")
    
