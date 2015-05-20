from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import sys

def check_sorted(sort_list):
    for i in range(len(sort_list)-1):
        if sort_list[i] > sort_list[i+1]:
            return False
    return True

def net_sort(sort_list, compares):
    for cmp1, cmp2 in compares:
        if sort_list[cmp1] > sort_list[cmp2]:
            sort_list[cmp1], sort_list[cmp2] = sort_list[cmp2], sort_list[cmp1]
    return sort_list

def generate_zero_one_inputs(size):
    input_stack = [0] * size
    while True:
        yield input_stack.copy()
        top_bit = input_stack[-1]
        if top_bit == 0:
            input_stack.pop()
            input_stack.append(1)
            continue

        while input_stack and input_stack[-1] == 1:
            input_stack.pop()
        if not input_stack:
            break

        input_stack.pop()
        input_stack.append(1)
        for i in range(size-len(input_stack)):
            input_stack.append(0)

def verify_input(input_tuple):
    input_list, compares = input_tuple
    net_sort(input_list, compares)
    return check_sorted(input_list)

def main():
    parallel_type = sys.argv[1] if len(sys.argv)>1 else "serial"
    mapfunc = map
    executor = None
    
    if parallel_type == "thread":
        executor = ThreadPoolExecutor(max_workers=7)
        mapfunc = executor.map
    elif parallel_type == "process":
        executor = ProcessPoolExecutor(max_workers=7)
        mapfunc = executor.map

    ###
        
    input_lines = sys.stdin.read().split('\n')
    num_wires, num_compares = [int(x) for x in input_lines[0].split()]

    compares = []
    for input_line in filter(lambda x: x, input_lines[1:]):
        line1, line2 = [int(x) for x in input_line.split()]
        compares.append( (line1, line2) )

    zero_one_inputs = generate_zero_one_inputs(num_wires)
        
    for valid in mapfunc(verify_input, [(zo_in, compares) for zo_in in zero_one_inputs]):
        if not valid:
            print("Invalid network")
            break
    else:
        print("Valid network")

    if executor:
        executor.shutdown()

if __name__ == '__main__': main()
