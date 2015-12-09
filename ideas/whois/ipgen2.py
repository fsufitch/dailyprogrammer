import ipaddress, random, string, sys

mask32 = 2**32-1
WORDS = [line.strip() for line in open('unix_words.txt') if line.strip().isalpha()]

def gen_names(num=250):
    titles = [x for x in WORDS if x[0].isupper()]
    words = [x for x in WORDS if x[0].islower()]
    suffixes = ["Inc", "LLC", "SRL", "PLC", "Institute", "International", "Association", "Union", "Party", "Committee"]
    prefixes = ["University of", "National", "Center for", "National Center for", "First",
                "United", "Republic of", "Democratic Republic of", "People's Republic of", ]
    names = []

    funcs = {
        'person': lambda: "%s %s" % (random.choice(titles), random.choice(titles)),
        'company_s1': lambda: " ".join([random.choice(WORDS).title(), random.choice(suffixes)]),
        'company_s2': lambda: " ".join([random.choice(WORDS).title(), random.choice(WORDS).title(), random.choice(suffixes)]),
        'company_p1': lambda: " ".join([random.choice(prefixes), random.choice(words).title()]),
        'company_p2': lambda: " ".join([random.choice(prefixes), random.choice(words).title(), random.choice(words).title()]),
    }

    for n in range(num):
        names.append(random.choice(list(funcs.values()))())

    while True:
        yield random.choice(names)

def make_ip(network):
    num = random.randrange(1, mask32)
    masked_net = int(network.network_address) & int(network.netmask)
    masked_host = num & int(network.hostmask)
    return ipaddress.ip_address(masked_net | masked_host)

def make_ip_range(network):
    ip1, ip2 = make_ip(network), make_ip(network)
    return min(ip1, ip2), max(ip1, ip2)

def netmask_int(bits):
    return (2**bits-1) << (32-bits)

names = gen_names()

for cluster in range(int(sys.argv[1])):
    base_ip = make_ip(ipaddress.ip_network("0.0.0.0/0"))
    masks = list(range(30))
    for masksize in range(int(sys.argv[2])):
        masksize = random.choice(masks)
        net_ip = ipaddress.ip_address(int(base_ip) & netmask_int(masksize))
        net = ipaddress.ip_network(net_ip.compressed + "/" + str(masksize))
        ip1, ip2 = make_ip_range(net)
        name = next(names)
        print(ip1.compressed, ip2.compressed, name)
        
