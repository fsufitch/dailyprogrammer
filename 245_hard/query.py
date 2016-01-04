import multiprocessing, sqlite3, sys

from concurrent.futures import ProcessPoolExecutor

def ipv4_to_int(ipstring):
    parts = [int(part) for part in ipstring.split('.')]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + (parts[3] << 0)

SEARCH_CACHE = {}
ROW_CACHE = {}

def get_row(c, rownum):
    global ROW_CAHCE
    if rownum not in ROW_CACHE:
        #c.execute("SELECT startip, endip, name FROM ip_ranges WHERE rowid=?", (rownum,))
        c.execute("SELECT netip, mask, name FROM ip_ranges WHERE rowid=?", (rownum,))
        ROW_CACHE[rownum] = c.fetchone()
    return 1, ROW_CACHE[rownum]

def get_subnet_row(c, netip, mask):
    global ROW_CAHCE
    if (netip, mask) not in ROW_CACHE:
        c.execute("SELECT netip, mask, name FROM ip_subnets WHERE netip=? AND mask=?", (netip, mask))
        ROW_CACHE[netip, mask] = c.fetchone()
    return 1, ROW_CACHE[netip, mask]

def get_smallest_net(c, netips):
    query = """SELECT netip, mask, name FROM ip_subnets 
                WHERE netip IN ({placeholders})
                ORDER BY mask DESC
                LIMIT 1"""
    query = query.format(placeholders = ','.join(['?'] * len(netips)))
    c.execute(query, netips)
    return 1, c.fetchone()

def subnet_search(c, ip_int):
    global SEARCH_CACHE
    q_count = 0
    if ip_int in SEARCH_CACHE:
        return SEARCH_CACHE[ip_int]
    
    netips = []
    for mask_guess in range(32, 0, -1):
        shift = 32 - mask_guess
        netip = (ip_int >> shift) << shift
        netips.append(netip)

    q, row = get_smallest_net(c, netips)
    q_count += q
    
    if row is not None:
        return q_count, row[2]
    return q_count, None
        
"""
def intersearch_db(c, ip_int, fromrow, torow):
    global SEARCH_CACHE, ROW_CACHE
    if ip_int in SEARCH_CACHE:
        return 0, SEARCH_CACHE[ip_int]
    
    if torow - fromrow < 1:
        return 0, None

    if torow - fromrow == 1:
        q, rowdata = get_row(c, fromrow)
        if rowdata[0] <= ip_int <= rowdata[1]:
            return q, rowdata[2]
        else:
            return q, None
    
    query_inc = 0

    #midrow = (fromrow + torow) // 2

    q, fromrow_data = get_row(c, fromrow)
    query_inc += q
    q, torow_data = get_row(c, torow-1)
    query_inc += q

    midrow = fromrow + (torow - fromrow) * ( (ip_int - fromrow_data[0]) / (torow_data[1] - fromrow_data[0]) )
    midrow = int(midrow)

    q, midrow_data = get_row(c, midrow)
    query_inc += q

    startip, endip, name = midrow_data
        
    if ip_int < startip:
        print(fromrow, midrow, torow, "down")
        queries, result = intersearch_db(c, ip_int, fromrow, midrow)
    elif ip_int > endip:
        print(fromrow, midrow, torow, "up")
        queries, result = intersearch_db(c, ip_int, midrow+1, torow)
    else:
        SEARCH_CACHE[ip_int] = name
        queries, result = 0, name

    return queries + query_inc, result
"""


#####

def main():
    dbpath = sys.argv[1]
    querypath = sys.argv[2]

    with open(querypath) as f:
        queries = f.readlines()
    
    queries = [q.strip() for q in queries]

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    #c.execute("SELECT COUNT(*) FROM ip_ranges")
    c.execute("SELECT COUNT(*) FROM ip_subnets")
    num_rows = c.fetchone()[0]

    counts = {}
    total_queries = 0
    for query in queries:
        query_int = ipv4_to_int(query)
        #query_count, name = intersearch_db(c, query_int, 1, num_rows+1)
        query_count, name = subnet_search(c, query_int)
        if not name:
            name = '<unknown>'
        
        total_queries += query_count
        counts[name] = counts.get(name, 0) + 1
    
    outputs = [(v, k) for k, v in counts.items()]
    outputs.sort(reverse=True)
    for count, name in outputs:
        print("%s - %s" % (count, name))

    print("Total DB queries over %d rows: %d (%.2f/query)" % (num_rows, total_queries, total_queries/len(queries)))

if __name__ == "__main__": main()
