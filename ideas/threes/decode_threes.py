import sys

def ternary_to_decimal(digits):
    dec = 0
    for i, digit in enumerate(reversed(digits)):
        dec += digit * (3 ** i)
    return dec

# =====

words = map(lambda x: x.strip().lower(), open(sys.argv[1]).readlines())

wordtree = {'word_complete': False}

for word in words:
    currnode = wordtree
    for char in word:
        if char not in currnode:
            currnode[char] = {'word_complete': False}
        currnode = currnode[char]
    currnode['word_complete'] = True

def partial_word(word):
    node = wordtree
    for char in word:
        if char not in node:
            return False
        node = node[char]
    return True

def complete_word(word):
    node = wordtree
    for char in word:
        if char not in node:
            return False
        node = node[char]
    return node.get('word_complete', False)

# =====

N = int(input("Start number? "))

states = [{
    'word': '',
    'N': N,
    'digit_buffer': [],
}]

solution_word = None

while states:
    current_state = states.pop()
    #states = states[1:]
    
    if current_state['N'] < 1:
        continue
    if current_state['N'] == 1:
        if complete_word(current_state['word']):
            solution_word = current_state['word']
            break
        continue
    
    moves = {
        0: [0],
        1: [-1, 2],
        2: [-2, 1],
    } [current_state['N'] % 3]
    
    for move in moves:
        newbuf = current_state['digit_buffer'] + [abs(move)]
        dec = ternary_to_decimal(newbuf)

        if dec > 255: # Not ASCII
            continue

        # First, try to not form a new letter
        states.append( {
            'word': current_state['word'],
            'N': (current_state['N'] + move) // 3,
            'digit_buffer': newbuf,
        })

        # Then try to form a new letter from the buffer

        newword = current_state['word'] + chr(dec)
        if partial_word(newword):
            states.append( {
                'word': newword,
                'N': (current_state['N'] + move) // 3,
                'digit_buffer': [],
            })

if solution_word:
    print('Solution:', solution_word)
else:
    print("No solution found!")
