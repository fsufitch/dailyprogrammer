from random import randrange

N = 5000000
R = 200000

print(N)
for i in range(R):
    print(randrange(0,N), randrange(0,N))
