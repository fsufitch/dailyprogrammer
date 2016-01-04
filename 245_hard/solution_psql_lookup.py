import getpass, pg8000, sys

infile = sys.argv[1]

server, user, pword = open('creds.txt').read().strip().split(':')
#server = input("Server: ")
#user = input("User: ")
#pword = getpass.getpass()

conn = pg8000.connect(host=server, user=user, password=pword)
curs = conn.cursor()

counts = {}

def ip_to_int(ipstring):
    parts = [int(p) for p in ipstring.split('.')]
    return (parts[0] << 24) + (parts[1] << 16) + (parts[2] << 8) + (parts[3] << 0)

curs.execute("CREATE TEMPORARY TABLE lookup_ips (lookupip numeric(10));")

insertbuf = []
for line in open(sys.argv[1]):
    ip = line.strip()
    if not ip: continue
    ip = ip_to_int(ip)
    insertbuf.append(ip)
    if len(insertbuf) > 500:
        curs.execute("INSERT INTO lookup_ips VALUES " + 
               ', '.join(["({})".format(i) for i in insertbuf]))
        insertbuf = []
        print("inserted")

if insertbuf:
    curs.execute("INSERT INTO lookup_ips VALUES " + 
                 ', '.join(["({})".format(i) for i in insertbuf]))

print("lookup...")
curs.execute("""SELECT COUNT(*), r.name 
                  FROM lookup_ips as l
                  INNER JOIN ip_ranges as r
                    ON l.lookupip > r.startip AND l.lookupip < r.endip
                  GROUP BY r.name
                  ORDER BY COUNT(*) DESC
""");

for row in curs.fetchall():
    count, name = row
    print(count, name)
