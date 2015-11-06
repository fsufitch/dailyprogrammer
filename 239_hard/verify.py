import sys

def ternary(i):
     if i==0: return []
     return ternary(i//3) + [i%3]

def dec(tern_list, p=0):
    if tern_list:
        return tern_list[-1] * 3**p + dec(tern_list[:-1], p+1)
    else:
        return 0

N = int(sys.stdin.readline().strip())

for line in sys.stdin.readlines():
    line = line.strip()
    tern_chars = list(map(ternary, [ord(c) for c in line]))
    terns = []
    for tern_char in tern_chars:
        terns += tern_char

    n = N
    
    real_moves = []
    for tern_seq in tern_chars:
        #print(chr(dec(tern_seq)))
        for move in tern_seq:
            if (n-move) % 3 == 0:
                move = -1 * move
            real_moves.append(move)
            n = (n + move) // 3
        
    if n == 1:
        print("{} -> good".format(line))
    else:
        print("{} -> {} -> {}".format(line, real_moves, n))
    
