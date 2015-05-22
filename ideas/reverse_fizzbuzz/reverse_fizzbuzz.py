import math, sys

def get_divisors(total, times_in):
    # X // ? = Y
    lower_bound_incl = math.ceil(total / (times_in + 1))
    upper_bound_excl = math.floor(total / times_in)
    print(total, times_in, lower_bound_incl, upper_bound_excl)
    yield from range(lower_bound_incl, upper_bound_excl)

num_words, max_count = [int(x) for x in sys.stdin.readline().split()]
fizz_lines = [x.split() for x in sys.stdin.read().split('\n')]

fizz_count = {}
for line in fizz_lines:
    for word in line:
        if not word in fizz_count:
            fizz_count[word] = 0
        fizz_count[word] += 1

fizz_guess = {}
for word in fizz_count:
    fizz_guess[word] = max_count // fizz_count[word]

guess_set = set()
for word in fizz_guess:
    for divisor in get_divisors(max_count, fizz_guess[word]):
        if divisor not in guess_set: break
    else:
        raise Exception("No solution!")
    fizz_guess[word] = divisor
    guess_set.add(divisor)

for word in fizz_guess:
    print(word, fizz_guess[word])    
