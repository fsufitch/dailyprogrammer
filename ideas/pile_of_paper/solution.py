import sys

class Rectangle(object):
    def __init__(self, color, col, row, width, height):
        self.color = color
        self.col = col
        self.row = row
        self.width = width
        self.height = height

    @property
    def top(self): return self.row
    @property
    def left(self): return self.col
    @property
    def bottom(self): return self.row + self.height
    @property
    def right(self): return self.col + self.width
    @property
    def area(self): return self.width * self.height
    
    def __repr__(self):
        text = "<Rectangle {id} C:{color} @ ({left},{top}) size {w}x{h} A={area}>"
        return text.format(id = id(self),
                           color = self.color,
                           left = self.left,
                           top = self.top,
                           w = self.width,
                           h = self.height,
                           area = self.area,
                       )
    
    def __contains__(self, rect):
        # Quick check if another rectacle is perfectly contained
        return (self.left <= rect.left and
                self.right >= rect.right and
                self.top <= rect.top and
                self.bottom >= rect.bottom)
    
    def intersect_vertical(self, col, row1, row2):
        if col < self.left or col > self.right:
            return False
        if row1 >= self.top and row1 < self.bottom:
            return True
        if row2 > self.top and row2 <= self.bottom:
            return True
        if row1 <= self.top and row2 >= self.bottom:
            return True
        return False

    def intersect_horizontal(self, col1, col2, row):
        if row < self.top or row > self.bottom:
            return False
        if col1 >= self.left and col1 < self.right:
            return True
        if col2 > self.left and col2 <= self.right:
            return True
        if col1 <= self.left and col2 >= self.right:
            return True
        return False

    def intersects(self, rect):
        return (self.intersect_vertical(rect.left, rect.top, rect.bottom) or
                self.intersect_vertical(rect.right, rect.top, rect.bottom) or
                self.intersect_horizontal(rect.left, rect.right, rect.top) or
                self.intersect_horizontal(rect.left, rect.right, rect.bottom) )

    def break_subrects(self, rect):
        if self in rect:
            return set() # Perfect overlap means nothing of us is left

        if not self.intersects(rect):
            return set([self])
        
        #      w1   w2   w3
        #    +----+----+----+
        # h1 | 1  | 8  | 7  |
        #    +----+----+----+
        # h2 | 2  |rect| 6  |
        #    +----+----+----+
        # h3 | 3  | 4  | 5  |
        #    +----+----+----+

        w1 = rect.left - self.left
        w3 = self.right - rect.right
        w2 = self.width - max(w1, 0) - max(w3, 0)

        h1 = rect.top - self.top
        h3 = self.bottom - rect.bottom
        h2 = self.height - max(h1, 0) - max(h3, 0)
        
        # 8 possible rects, CCW from top left
        subrect_dimensions = [(self.left, self.top, w1, h1),
                              (self.left, rect.top, w1, h2),
                              (self.left, rect.bottom, w1, h3),
                              (rect.left, rect.bottom, w2, h3),
                              (rect.right, rect.bottom, w3, h3),
                              (rect.right, rect.top, w3, h2),
                              (rect.right, self.top, w3, h1),
                              (rect.left, self.top, w2, h1)]
        subrects = set()
        for left, top, width, height in subrect_dimensions:
            if width <= 0 or height <= 0:
                continue # This subrect doesn't exist
            subrect = Rectangle(self.color, left, top, width, height)
            subrects.add(subrect)
        return subrects
        
def get_rects():
    with open(sys.argv[1]) as infile:
        cols, rows = infile.readline().split()
        cols = int(cols.strip())
        rows = int(rows.strip())
        base_rect = Rectangle(0, 0, 0, cols, rows)
        yield base_rect
        for line in infile:
            color, col, row, width, height = [int(chunk.strip()) for chunk in line.split()]
            yield Rectangle(color, col, row, width, height)

def main():
    real_rects = set()
    cnt = 0
    for rect in get_rects():
        split_rects = set()
        split_rects.add(rect)
        for existing_rect in real_rects:
            print("%s splitting %s:" % (rect,existing_rect))
            new_rects = existing_rect.break_subrects(rect)
            for prect in new_rects:
                print("    ", prect)
            split_rects.update(new_rects)
        real_rects = split_rects
        cnt += 1
        print(cnt, "Current rect count:",len(real_rects))

    colors = {}
    for rect in real_rects:
        #print("RECT: ",rect)
        colors[rect.color] = colors.get(rect.color, 0) + rect.area
    #print(len(real_rects), "real rects")

    for rect1 in real_rects:
        for rect2 in real_rects:
            if rect1 is rect2: continue
            #if rect1.intersects(rect2):
            #    print("Intersect!", rect1, rect2)

    for color, area in sorted(list(colors.items())):
        print("%s %s" % (color, area))

    print("Total area:", sum(colors.values()))
    
if __name__ == '__main__': main()
