import queue, random, sys

# Take input
if len(sys.argv) > 1:
    N  = int(sys.argv[1])
else:
    N = int(input("N? "))

visited_states = set()   # Set of: (value, score)
solution = None

first_step = {
    "value": N,
    "from": None,
    "move": None,
    "score": 0,
}

to_process = queue.PriorityQueue()  # Pqueue of (abs_score, step)
to_process.put( (0, first_step) )

# While there are steps to process
while not to_process.empty():
    _, step = to_process.get()

    # Check if this is a solution
    if step["value"] == 1:
        if step["score"] == 0:
            solution = step
            break
        continue

    # Record this value/score state; if already visited, skip
    score_key = (step["value"], step["score"])
    if score_key in visited_states:
        continue
    visited_states.add(score_key)
    
    # Calculate what moves are available based on value mod 3
    move_options = {
        0: (0,),
        1: (-1, 2),
        2: (-2, 1),
    }[step["value"] % 3]
    
    if step["value"] == 2: # Edge case, can't reach zero
        move_options = (1,)
    
    # Create and record next steps
    for move in move_options:
        next_step = {
            "value": (step["value"] + move) // 3,
            "from": step,
            "move": move,
            "score": step["score"] + move
        }
        abs_score = abs(next_step["score"])
        abs_score += random.random() / 100000  # Hack to avoid comparing the second tuple element (dicts)
        to_process.put( (abs_score, next_step) )

# Impossible?
if not solution:
    print("Impossible")
    exit()

# Process into printable lines (moves are offset by 1)
output = []
current_step = solution
last_move = None
while current_step:
    if last_move is not None:
        output.append( (current_step["value"], last_move) )
    else:
        output.append( (current_step["value"],) )
    last_move = current_step["move"]
    current_step = current_step["from"]

# Print
for line in reversed(output):
    print(*line)

# Done!
