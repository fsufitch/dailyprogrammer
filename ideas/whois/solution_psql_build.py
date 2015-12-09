import getpass, pg8000, sys

infile = sys.argv[1]

server = input("Server: ")
user = input("User: ")
pword = getpass.getpass()

conn = pg8000.connect(host=server, user=user, password=pword)
curs = conn.cursor()

print("Dropping current ranges...")
curs.execute("DELETE FROM ip_ranges")

def read_ranges(filename):
    ranges = set()
    with open(filename) as f:
        for line in f:
            startip, endip, data = line.strip().split(' ', 2)
            if (startip, endip) in ranges:
                continue
            ranges.add( (startip, endip) )
            yield startip, endip, data
    print(" Done reading.")

def group(num, iterator):
    g = []
    for item in iterator:
        g.append(item)
        if len(g) >= num:
            yield g
            g = []
    yield g

print("Creating iterator...")

N = 500
total = 0
groups = group(N, read_ranges(infile))

print("Inserting new ranges...")
for g in groups:
    print("Inserting %d... " % len(g))
    curs.executemany("INSERT INTO ip_ranges VALUES (%s, %s, %s)", g)
    total += len(g)
    print("Done. Total: %d" % total)

print("Committing...")
curs.commit()
print("Done.")
