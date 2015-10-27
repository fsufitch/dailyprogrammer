import math, queue, string, sys

LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def create_g_strings(length):
    if length == 1:
        yield 'g'
        yield 'G'
    else:
        for g in create_g_strings(length-1):
            yield 'g' + g
            yield 'G' + g

def create_encode_map(letters):
    encode_map = {}
    g = create_g_strings(math.ceil(math.log(len(letters), 2)))
    
    for letter in letters:
        encode_map[letter] = next(g)

    return encode_map

def encode(data):
    used_letters = set(LETTERS).intersection(set(data))

    encode_map = create_encode_map(used_letters)

    print(' '.join(' '.join([l, g]) for l,g in sorted(encode_map.items())) )

    for char in data:
        sys.stdout.write( encode_map.get(char, char) )

################

def create_hencode_map(letter_freqs):
    node_queue = queue.PriorityQueue()
    for frequency, letter in letter_freqs:
        node_queue.put( (frequency, letter, '', '') )
        
    while True:
        node1 = node_queue.get()
        if len(node_queue.queue) == 0: # we're done
            root_node = node1
            break

        node2 = node_queue.get()
        node_queue.put( (node1[0]+node2[0], '', node1, node2) )
    
    node_stack = [('', root_node)]
    encode_map = {}
    while node_stack:
        g_seq, node = node_stack.pop()
        if node[1]: # This is a letter "leaf"
            encode_map[node[1]] = g_seq
            continue
        node_stack.append( (g_seq + 'g', node[2]) )
        node_stack.append( (g_seq + 'G', node[3]) )
    return encode_map

def hencode(data):
    used_letters = set(LETTERS).intersection(set(data))
    letter_freqs = [ (data.count(letter), letter) for letter in used_letters ]

    encode_map = create_hencode_map(letter_freqs)
    print(' '.join(' '.join([l, g]) for l,g in sorted(encode_map.items())) )

    for char in data:
        sys.stdout.write( encode_map.get(char, char) )

################

def create_decode_map(key_line):
    line_items = key_line.split()
    line_items.reverse()
    decode_map = {}
    while line_items:
        letter, g_seq = line_items.pop(), line_items.pop()
        decode_map[g_seq] = letter
    return decode_map

def decode(data):
    first_newline = data.find('\n')
    decode_map = create_decode_map(data[:first_newline])
    data = data[first_newline+1:]
    buf = ''
    for char in data:
        if char in ['G', 'g']:
            buf += char
            if buf in decode_map:
                sys.stdout.write(decode_map[buf])
                buf = ''
        else:
            if buf:
                raise Exception('Incomplete G buffer: %s' % buf)
            sys.stdout.write(char)
    if buf:
        raise Exception('Incomplete G buffer: %s' % buf)

################

def main():
    if len(sys.argv) < 1 or sys.argv[1] not in ['encode', 'hencode', 'decode']:
        print("Please specify encode/hencode/decode command")
        exit()
        
    if len(sys.argv) > 2:
        with open(sys.argv[2]) as f:
            data = f.read()
    else:
        data = sys.stdin.read()

    if sys.argv[1] == 'encode':
        encode(data)
    elif sys.argv[1] == 'hencode':
        hencode(data)
    else:
        decode(data)

if __name__ == '__main__':
    main()
