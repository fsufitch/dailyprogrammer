import random, sys

rows = int(sys.argv[1])
cols = int(sys.argv[2])
zombies = int(sys.argv[3])

print(rows, cols)

positions = set()

while len(positions) < zombies:
    row = random.randrange(0, rows)
    col = random.randrange(0, cols)
    positions.add( (row, col) )

for row, col in positions:
    print(row, col)

