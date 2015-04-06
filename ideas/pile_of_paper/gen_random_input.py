import sys, random

if len(sys.argv) < 2:
    print("Args: width height num_colors num_rects")
    sys.exit()

width = int(sys.argv[1])
height = int(sys.argv[2])
num_colors = int(sys.argv[3])
num_rects = int(sys.argv[4])

print("%s %s" % (width, height))

for i in range(num_rects):
    col1 = random.randint(0, width-5)
    col2 = random.randint(col1+1, width)
    row1 = random.randint(0, height-5)
    row2 = random.randint(row1+1, height)
    color = random.randint(0, num_colors)

    rect_width = col2 - col1
    rect_height = row2 - row1
    
    print("%s %s %s %s %s" % (color, col1, row1, rect_width, rect_height))
    
