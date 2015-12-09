import getpass, pg8000, sys

infile = sys.argv[1]

server = input("Server: ")
user = input("User: ")
pword = getpass.getpass()

conn = pg8000.connect(host=server, user=user, password=pword)
curs = conn.cursor()

counts = {}

for line in open(sys.argv[1]):
    ip = line.strip()
    curs.execute("""SELECT startip, endip, data FROM ip_ranges 
                     WHERE startip<%s::inet AND endip>%s::inet
                     ORDER BY endip-startip ASC
                     LIMIT 1""",
                 (ip, ip))
    result = curs.fetchone()
    result = result[2] if result else "<unknown>"

    counts[result] = counts.get(result, 0) + 1

countlist = [(v,k) for k,v in counts.items()]
countlist.sort()
countlist.reverse()
for c, name in countlist:
    print("%d - %s" % (c, name))

