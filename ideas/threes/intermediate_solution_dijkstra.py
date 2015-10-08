import sys

# Take input
if len(sys.argv) > 1:
    N  = int(sys.argv[1])
else:
    N = int(input("N? "))

best_scores = {}
best_solution = None

first_step = {
    "value": N,
    "from": None,
    "move": None,
    "score": 0,
}

to_process = [first_step]

# While there are steps to process
while to_process:
    step = to_process.pop()

    # Check if this is a solution
    if (step["value"] == 1):
        if best_solution == None or best_solution["score"] < step["score"]:
            best_solution = step
        continue

    # Record this score for this value; if it's too low, skip
    if (step["value"] in best_scores) and (step["score"] <= best_scores[step["value"]]):
        continue # Worse or equal to what we've seen before; ignore
    best_scores[step["value"]] = step["score"]
    
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
            "score": step["score"] + (-1 if move != 0 else 0)
        }
        to_process.append(next_step)

# Process into printable lines (moves are offset by 1)
output = []
current_step = best_solution
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
