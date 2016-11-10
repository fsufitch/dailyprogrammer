import re
from functools import reduce

funcs = {
    '+': lambda stack: stack.pop() + stack.pop(),
    '-': lambda stack: (lambda y, x: x - y)(stack.pop(), stack.pop()),
    '*': lambda stack: stack.pop() * stack.pop(),
    '/': lambda stack: (lambda y, x: x / y)(stack.pop(), stack.pop()),
    '//': lambda stack: (lambda y, x: x // y)(stack.pop(), stack.pop()),
    '^': lambda stack: (lambda y, x: x ** y)(stack.pop(), stack.pop()),
    '%': lambda stack: (lambda y, x: x % y)(stack.pop(), stack.pop()),
    '!': lambda stack: reduce(lambda x, y: x * y, range(1, 1 + stack.pop())),
}

is_int_regex = re.compile('^-?[0-9]+$')
is_float_regex = re.compile('^-?[0-9.]+$')


def main():
    input_data = input('RPN expression? ')
    stack = []
    try:
        for token in input_data.split():
            if not token:
                continue
            if is_int_regex.match(token):
                stack.append(int(token))
            elif is_float_regex.match(token):
                stack.append(float(token))
            elif token in funcs:
                stack.append(funcs[token](stack))
            else:
                print('Could not process token', token)
                return
    except IndexError:
        print('Insufficient operands on the stack')
        return
    if len(stack) > 1:
        print('More than one number on stack after calculation:', stack)
    else:
        print(stack[0])

if __name__ == '__main__':
    main()
