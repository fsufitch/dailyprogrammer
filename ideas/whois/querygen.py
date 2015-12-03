import ipaddress, random, sys

mask32 = 2**32-1

def make_ip(network):
    num = random.randrange(1, mask32)
    masked_net = int(network.network_address) & int(network.netmask)
    masked_host = num & int(network.hostmask)
    return ipaddress.ip_address(masked_net | masked_host)

for i in range(int(sys.argv[1])):
    print(make_ip(ipaddress.ip_network('0.0.0.0/0')))
