import sys

def get_numbers(fname):
    with open(fname) as infile:
        for line in infile:
            for number in line.split():
                yield number

def get_uniques(numbers):
    seen = set()
    for number in numbers:
        if number not in seen:
            seen.add(number)
            yield number

def main():
    numbers = get_numbers(sys.argv[1])
    uniques = get_uniques(numbers)
    print(' '.join(uniques))

if __name__ == '__main__':
    main()
