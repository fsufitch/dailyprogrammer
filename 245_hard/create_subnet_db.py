import math, os, sqlite3, sys

def mask(size):
    return (1 << size) - 1

def make_linked_list(iterable):
    curr = None
    for item in reversed(iterable):
        curr = (item, curr)
    return curr

def flatten_ranges(ranges):
    print("making linked list")
    range_ll = make_linked_list(sorted(ranges))
    print("done making ll")

    reduced_ranges = []
    
    while range_ll:
        if range_ll[1] == None: # last element
            reduced_ranges.append( range_ll[0] )
            break
        startip1, endip1, name1, size1 = range_ll[0]
        startip2, endip2, name2, size2 = range_ll[1][0]

        range_ll = range_ll[1][1] # forget about two nodes

        if endip1 < startip2: # they don't overlap; range 1 is done
            reduced_ranges.append( (startip1, endip1, name1, size1) )
            range_ll = ((startip2, endip2, name2, size2), range_ll)
        else:
            # resize one of the ranges
            if size1 <= size2:
                new1 = startip1, endip1, name1, size1
                new2 = endip1 + 1, endip2, name2, size2
            else:
                new1 = startip1, startip2 - 1, name1, size1
                new2 = startip2, endip2, name2, size2

            range_ll = (new1, (new2, range_ll))

    return reduced_ranges

top_sub_length = 0
def range_to_subnets(iprange):
    startip, endip, name, size = iprange
    if endip - startip < 0:
        return [] # whoops
    if endip - startip == 0: # one ip
        #return [(startip, endip, name)]
        return [(startip, 32, name)]

    # Find mask for biggest subnet that would fit in the range
    for masksize in range(32, -1, -1):
        subnet_start = (startip >> masksize) << masksize
        if subnet_start < startip: continue

        m = mask(masksize)
        subnet_end = startip | m
        if subnet_end > endip: continue

        break
    else:
        raise SystemError("omgwtf, this can't happen")

    subnet_mask = 32 - masksize
    #subnet = subnet_start, subnet_end, name
    subnet = subnet_start, subnet_mask, name
    
    pre_subnets = range_to_subnets( (startip, subnet_start-1, name, size) )
    post_subnets = range_to_subnets( (subnet_end+1, endip, name, size) )

    return pre_subnets + [subnet] + post_subnets

def build_db(subnets):
    conn = sqlite3.connect(sys.argv[2])
    c = conn.cursor()

    print("setting up table and index")
    # c.execute("""CREATE TABLE ip_ranges 
    #              (startip unsigned big int, endip unsigned big int, name text)""")
    # c.execute("""CREATE INDEX ip_range_index 
    #              ON ip_ranges (startip ASC, endip ASC, name)""")

    c.execute("""CREATE TABLE ip_subnets 
                 (netip unsigned big int, mask int, name text)""")
    c.execute("""CREATE INDEX ip_subnet_index 
                 ON ip_subnets (netip, mask DESC, name)""")
    
    print("starting insert operations")
    INCREMENT = 10000
    total = 0
    for i in range(0, len(subnets), INCREMENT):
        buf = subnets[i:i+INCREMENT]
        total += len(buf)
        print("inserting %d records; total: %d/%d" % (len(buf), total, len(subnets)))
        #c.executemany("INSERT INTO ip_ranges VALUES (?,?,?)", buf)
        c.executemany("INSERT INTO ip_subnets VALUES (?,?,?)", buf)
        
    print("committing")
    conn.commit()

def ipv4_to_int(ipstring):
    parts = [int(part) for part in ipstring.split('.')]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + (parts[3] << 0)
        
def main():
    assert sys.argv[2]
    f = open(sys.argv[1])
    ranges = []
    print("reading...")
    for line in f:
        line = line.strip()
        if not line: continue
        ip1, ip2, name = line.split(maxsplit=2)
        ip1 = ipv4_to_int(ip1)
        ip2 = ipv4_to_int(ip2)
        ranges.append( (ip1, ip2, name, ip2-ip1) )  # start, end, name, original size
    f.close()
        
    print("flattening %s" % len(ranges))
    flat_ranges = flatten_ranges(ranges)
    print("flattened %s" % len(flat_ranges))

    print("subnetting")
    subnets = []
    for r in flat_ranges:
        subnets += range_to_subnets(r)
        
    print("subnetted %s" % len(subnets))

    build_db(subnets)
    print("done")
    
        
if __name__ == "__main__": main()
