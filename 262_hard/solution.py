import copy, functools, heapq, itertools, sys

SIZE = 4

@functools.total_ordering
class GridState:
    def __init__(self, grid, src_move, num_moves):
        self.grid = grid
        self.move = src_move
        self.num_moves = num_moves
        self._dist = None
        self._hash = None

    def solution_distance(self):
        if self._dist is not None: return self._dist
        self._dist = 0
        for row in range(SIZE):
            for col in range(SIZE):
                target_row = (self.grid[row][col] - 1) // SIZE
                target_col = (self.grid[row][col] - 1) % SIZE
                drow = row - target_row
                dcol = col - target_col
                self._dist += abs(drow) + abs(dcol)
        return self._dist
        
    def __lt__(self, other):
        return self.solution_distance() < other.solution_distance()
    def __eq__(self, other):
        return self.solution_distance() == other.solution_distance()
    
    def __hash__(self):
        if self._hash is None:
            self._hash = hash(tuple(itertools.chain(*self.grid)))
        return self._hash
        
    def _swap(self, row, col, drow, dcol):
        if (row + drow < 0 or row + drow >= SIZE or
            col + dcol < 0 or col + dcol >= SIZE):
            return None
        newgrid = copy.deepcopy(self.grid)
        move = (self, newgrid[row][col], newgrid[row+drow][col+dcol])
        newgrid[row][col], newgrid[row+drow][col+dcol] = newgrid[row+drow][col+dcol], newgrid[row][col]
        return GridState(newgrid, move, self.num_moves+1)
    
    def next_states(self):
        for row in range(SIZE):
            for col in range(SIZE):
                for drow, dcol in ( (1,0), (-1,0), (0,1), (0,-1) ):
                    newstate = self._swap(row, col, drow, dcol)
                    if newstate is not None:
                        yield newstate

    def print_moves(self):
        if not self.move: return
        prev_state, move1, move2 = self.move
        prev_state.print_moves()
        print(move1, move2)

    def print_grid(self):
        for row in self.grid:
            print(' '.join(['%2.d' % n for n in row]))

def solve(grid):
    known_states = {} # hash -> state
    state_heap = []
    heapq.heappush(state_heap, GridState(grid, None, 0))
    while len(state_heap):
        state = heapq.heappop(state_heap)
        if int(state.solution_distance()) == 0: # done!
            return state

        for next_state in state.next_states():
            if (hash(next_state) not in known_states or
                known_states[hash(next_state)].num_moves > next_state.num_moves):
                known_states[hash(next_state)] = next_state
                heapq.heappush(state_heap, next_state)

    return None
                        
def main():
    grid = []
    with open(sys.argv[1]) as infile:
        grid = [list(map(int, line.split())) for line in infile.readlines()][:SIZE]

    solved_state = solve(grid)
    if solved_state:
        print("Solved in %s moves:" % solved_state.num_moves)
        solved_state.print_moves()
        solved_state.print_grid()
    else:
        print("No solution.")
        
        
if __name__ == '__main__': main()
