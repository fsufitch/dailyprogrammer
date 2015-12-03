import ipaddress, random, string, sys

mask32 = 2**32-1

def make_ip(network):
    num = random.randrange(1, mask32)
    masked_net = int(network.network_address) & int(network.netmask)
    masked_host = num & int(network.hostmask)
    return ipaddress.ip_address(masked_net | masked_host)

def make_ip_range(network):
    ip1, ip2 = make_ip(network), make_ip(network)
    return min(ip1, ip2), max(ip1, ip2)

def gen_names():
    while True:
        n = random.randrange(200, 2**20)
        for i in range(random.randrange(3, 20)):
            yield hex(n)[2:]
            n += 1

def netmask_int(bits):
    return (2**bits-1) << (32-bits)

names = gen_names()

for cluster in range(int(sys.argv[1])):
    base_ip = make_ip(ipaddress.ip_network("0.0.0.0/0"))
    masks = list(range(30))
    random.shuffle(masks)
    for masksize in masks[:int(sys.argv[2])]:
        net_ip = ipaddress.ip_address(int(base_ip) & netmask_int(masksize))
        net = ipaddress.ip_network(net_ip.compressed + "/" + str(masksize))
        ip1, ip2 = make_ip_range(net)
        name = next(names)
        print(ip1.compressed, ip2.compressed, name)
        
