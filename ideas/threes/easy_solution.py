import sys

# Take input
if len(sys.argv) > 1:
    N  = int(sys.argv[1])
else:
    N = int(input("N? "))


current = N  # Repeat until we get to 1
while current != 1:
    # Decide what move we take
    if current % 3 == 0:
        move = 0          # 0 if it's already divisible
    elif current % 3 == 1:
        move = -1         # -1 if it's 1 too high
    else:
        move = 1          # 1 otherwise

    # Print this step
    print(current, move)

    # Play the game and generate the next current value
    current = (current + move) // 3

# Print the last 1
print(current)

# Done!
