from random import randint

NUM_NUMS = 1000000
MIN = 0
MAX = 20

def gen_numbers():
    for i in range(NUM_NUMS):
        yield str(randint(MIN, MAX))

print(" ".join(gen_numbers()))
