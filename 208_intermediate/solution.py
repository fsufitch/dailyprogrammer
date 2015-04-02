import decimal, math, sys

def get_distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx*dx + dy*dy)

def round_rhu(num):
    dec = decimal.Decimal(num)
    no_fp_error = dec.quantize(decimal.Decimal('1e-3'))
    rounded = no_fp_error.quantize(decimal.Decimal(1), rounding=decimal.ROUND_HALF_UP)
    return rounded

class RadialGradient(object):
    def __init__(self, symbols, cx, cy, radius):
        self.symbols = list(symbols)
        self.center_x = cx
        self.center_y = cy
        self.radius = radius

        self.interval = self.radius / len(self.symbols)

    def get_symbol(self, x, y):
        distance = get_distance(self.center_x, self.center_y, x, y)

        sym_index = int(round_rhu(distance / self.interval))
        symbol = self.symbols[sym_index] if sym_index < len(self.symbols) else self.symbols[-1]
        return symbol
    
class LinearGradient(object):
    def __init__(self, symbols, x1, y1, x2, y2):
        self.symbols = list(symbols)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.grad_length = get_distance(x1, y1, x2, y2)
        self.interval = self.grad_length / len(self.symbols)

    def get_symbol(self, x, y):
        # Distance to x1,y1
        d1 = get_distance(self.x1, self.y1, x, y)

        # Distance to x2,y2
        d2 = get_distance(self.x2, self.y2, x, y)

        # Trig magic; see trig.jpg
        projected_distance = (d1**2 - d2**2 + self.grad_length**2) / (2 * self.grad_length)

        sym_index = int(round_rhu(projected_distance / self.interval))
        if sym_index < 0:
            symbol = self.symbols[0]
        elif sym_index >= len(self.symbols):
            symbol = self.symbols[-1]
        else:
            symbol = self.symbols[sym_index]
        return symbol

def main():
    fpath = sys.argv[1]
    with open(fpath) as infile:
        cols, rows = infile.readline().strip().split()
        cols = int(cols)
        rows = int(rows)

        symbols = infile.readline().rstrip('\r\n')
        
        grad_input = infile.readline().strip().split()
        if grad_input[0] == 'radial':
            gradient = RadialGradient(symbols,
                                      int(grad_input[1]),
                                      int(grad_input[2]),
                                      float(grad_input[3]))
        elif grad_input[0] == 'linear':
            gradient = LinearGradient(symbols,
                                      int(grad_input[1]),
                                      int(grad_input[2]),
                                      int(grad_input[3]),
                                      int(grad_input[4]))
        else:
            raise ValueError("Unknown gradient type: %s" % grad_input[0])

    for row in range(rows):
        chars = [gradient.get_symbol(col, row) for col in range(cols)]
        print(''.join(chars))
        
if __name__ == '__main__': main()
