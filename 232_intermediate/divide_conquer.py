import re, sys

def read_points():
    points = []
    f = sys.stdin
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
    count = int(f.readline().strip())
    reg = re.compile('\(([\.\dE-]+),\s*([\.\dE-]+)\)')
    for i in range(count):
        line = f.readline()
        x, y = reg.search(line).groups()
        x, y = float(x), float(y)
        points.append( (x,y) )

    if len(sys.argv) > 1:
        f.close()

    return points

def dist(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    dx = x1 - x2
    dy = y1 - y2
    d = dx * dx + dy * dy
    return d

def calculate_min_center(points, left_index, right_index, max_dist):
    # Calculate min distance for points up to max_dist away from middle point
    middle_index = (right_index + left_index) // 2
    left_points = []
    for i in range(len(points)): # Only up to 6 points due to geometry magic, but use len(points) for completeness
        left_i = middle_index - i - 1
        if left_i >= left_index and points[middle_index][0] - points[left_i][0] < max_dist:
            left_points.append(points[left_i])
        else:
            break

    right_points = []
    for i in range(len(points)): # Only up to 6 points due to geometry magic, but use len(points) for completeness
        right_i = middle_index + i
        if right_i < right_index and points[right_i][0] - points[middle_index][0] < max_dist:
            right_points.append(points[right_i])
        else:
            break

    if not (left_points and right_points):
        return None
    min_pair = left_points[0], right_points[0]
    min_dist = dist(*min_pair)
    for left_pt in left_points:
        for right_pt in right_points:
            if dist(left_pt, right_pt) < min_dist:
                min_pair = left_pt, right_pt
                min_dist = dist(*min_pair)
    
    return min_pair
        
def divide_conquer(points, left_index, right_index):
    assert right_index - left_index > 1
    if right_index - left_index == 2:
        # Just two, answer is obvious
        return points[left_index], points[left_index+1]
    if right_index - left_index == 3:
        # Just compare them!
        pt1, pt2, pt3 = points[left_index:right_index]
        pair_dists = [ 
            (dist(pt1, pt2), (pt1, pt2)),
            (dist(pt2, pt3), (pt2, pt3)),
            (dist(pt1, pt3), (pt1, pt3)),
        ]
        return min(pair_dists)[1]

    # Other cases can be recursive!
    middle_index = (right_index + left_index) // 2

    min_pair_left = divide_conquer(points, left_index, middle_index)
    min_pair_right = divide_conquer(points, middle_index, right_index)

    if dist(*min_pair_left) < dist(*min_pair_right):
        min_pair_lr = min_pair_left
        min_dist_lr = dist(*min_pair_left)
    else:
        min_pair_lr = min_pair_right
        min_dist_lr = dist(*min_pair_right)
    
    min_pair_center = calculate_min_center(points, left_index, right_index, min_dist_lr)
    if min_pair_center is not None and dist(*min_pair_center) < min_dist_lr:
        return min_pair_center
    else:
        return min_pair_lr

def main():
    points = read_points()
    points.sort()

    min_pair = divide_conquer(points, 0, len(points))

    print("%s, %s" % min_pair)

if __name__ == '__main__':
    main()
