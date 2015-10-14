import functools, itertools, math, sys

FIBS_CACHE = {}
def fib(f1, index):
    """ Calculate the index-th fib number if f(1)=f1. Use a dict cache. """
    if index == 0:
        return 0
    if index == 1:
        return f1
    if (f1, index) not in FIBS_CACHE:
        FIBS_CACHE[f1, index] = fib(f1, index-1) + fib(f1, index-2)
    return FIBS_CACHE[f1, index]

def find_fib_factor(n):
    """ Search the regular fib sequence for the highest factor of n (for lowest multiple)
    Return the index on success. If not found, return 1. """
    max_factor = 1
    for i in itertools.count(3): # Start search at 3rd number; 0 1 1 are uninteresting
        if n % fib(1, i) == 0:
            max_factor = i
        if fib(1, i) > n: # There can be no factors greater than this
            return max_factor

def main():
    if len(sys.argv)>1:
        N = sys.argv[1]
    else:
        N = input("Number to have in your fib sequence? ")

    N = int(N)

    fib_factor_index = find_fib_factor(N)
    fib_multiple = N // fib(1, fib_factor_index)

    fibs = [ str(fib(fib_multiple, i)) for i in range(fib_factor_index+1) ]
    print(" ".join(fibs))
    

if __name__ == "__main__":
    main()
