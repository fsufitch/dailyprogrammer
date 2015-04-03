import sys

def get_adjacent(locations, row, col):
    adjacent = [
        (row-1, col),
        (row+1, col),
        (row, col-1),
        (row, col+1),
        ]
    adjacent = [loc for loc in adjacent if loc in locations]
    return adjacent

def get_max_travel(locations, start_row, start_col, max_moves):
    # Use a list as a queue; item structure: (row, col, num_moves_so_far)
    borders_queue = [ (start_row, start_col, 0) ]
    traveled_locs = set( [(start_row, start_col)] )

    while borders_queue:
        row, col, moves = borders_queue.pop(0)
        adjacent = get_adjacent(locations, row, col)

        for next_row, next_col in adjacent:
            if (next_row, next_col) in traveled_locs:
                continue # Ignore it if we've already been there
            if locations[next_row, next_col] != "O":
                continue # Must be empty
            if moves < max_moves: # If we have moves left
                traveled_locs.add( (next_row, next_col) )
                borders_queue.append( (next_row, next_col, moves+1) )

    return traveled_locs

def print_locations(rows, cols, locations, travel, hero_row, hero_col):
    for row in range(rows):
        chars = []
        for col in range(cols):
            char = locations[row, col]
            if (row, col) == (hero_row, hero_col):
                char = "H"
            elif (row, col) in travel:
                char = "W"
            chars.append(char)
        print("".join(chars))

def main():
    inpath = sys.argv[1]
    with open(inpath) as infile:
        rows, cols = infile.readline().strip().split()
        rows = int(rows)
        cols = int(cols)

        locations = {}
        for r in range(rows):
            line = infile.readline().rstrip('\n')
            for c in range(cols):
                locations[r, c] = line[c]

        start_row, start_col, max_moves = infile.readline().strip().split()
        start_row = int(start_row)
        start_col = int(start_col)
        max_moves = int(max_moves)

    travel_locs = get_max_travel(locations, start_row, start_col, max_moves)

    print_locations(rows, cols, locations, travel_locs, start_row, start_col)

if __name__ == '__main__':
    main()
