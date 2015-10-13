import re, sys

def dist(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    dx = x1 - x2
    dy = y1 - y2
    return dx * dx + dy * dy

class DistanceDb(object):
    def __init__(self):
        self.points = {}
        self.min_dist = None
        self.min_pair = None

    def insert_point(self, new_pt):
        if new_pt in self.points:
            return
        point_map = {}
        ignore_pts = set()

        for pt in self.points:
            if pt in ignore_pts:
                continue
            d = dist(pt, new_pt)

            for next_pt in self.points[pt]:
                if self.points[pt][next_pt] > 2 * d:
                    ignore_pts.add(next_pt)

            point_map[pt] = d
            if not self.min_dist or d < self.min_dist:
                self.min_dist = d
                self.min_pair = (new_pt, pt)

        print(new_pt, len(point_map), len(self.points))
        self.points[new_pt] = point_map

def read_points():
    # Read with a generator to handle huge inputs
    f = sys.stdin
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    count = int(f.readline().strip())
    reg = re.compile('\(([\.\dE-]+),\s*([\.\dE-]+)\)')
    for i in range(count):
        line = f.readline()
        x, y = reg.search(line).groups()
        x, y = float(x), float(y)
        yield (x, y)

    if len(sys.argv) > 1:
        f.close()

def main():
    point_gen = read_points()
    db = DistanceDb()
    for pt in point_gen:
        db.insert_point(pt)

    print("%s, %s" % db.min_pair)

if __name__ == '__main__':
    main()
