import random, string, sys
wordsfile, rows, cols = sys.argv[1:4]
rows, cols = int(rows), int(cols)
with open(wordsfile) as f:
    lines = f.readlines()

words = [w.strip().upper() for w in lines if w.strip()]

grid = [[random.choice(string.ascii_uppercase) for i in range(cols)] for j in range(rows)]


for i in range(5*(rows+cols)): # arbitrary lol
    word = random.choice(words)
    r, c = random.randrange(0, rows), random.randrange(0, cols)
    dr, dc = random.choice([
        (0, 1), # horizontal
        (1, 0), # vertical
        (1, 1), # diagonal down
        (-1, 1), # diagonal up
    ])
    while word and (r>=0 and r<rows) and (c>=0 and c<cols):
        grid[r][c] = word[0]
        word = word[1:]
        r, c = r+dr, c+dc

print('\n'.join([''.join(row) for row in grid]))
