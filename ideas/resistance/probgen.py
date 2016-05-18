import string

WIDTH = 20
LETTERS = string.uppercase

grid = []
for i in range(WIDTH):
    row = []
    for j in range(WIDTH):
        row.append(LETTERS[i] + LETTERS[j])
    grid.append(row)

edges = []

for i in range(WIDTH):
    for j in range(WIDTH):
        if i < WIDTH-1:
            edges.append( (grid[i][j], grid[i+1][j], 10000) )
        if j < WIDTH-1:
            edges.append( (grid[i][j], grid[i][j+1], 10000) )

import itertools
print(' '.join(itertools.chain(*grid)))

for n1, n2, res in edges:
    print n1, n2, res
