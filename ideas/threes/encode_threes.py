import random

msg = input('Message? ')

def ternary(i):
     if i==0: return []
     return ternary(i//3) + [i%3]

tern = []
for char in msg:
    tern += ternary(ord(char))

print(tern)

number = 1

for increment in reversed(tern):
    if number > 3: # To prevent weirdness here
        increment = increment * random.choice([-1, 1])
    print(increment)
    number = number * 3 + increment

print(number)
