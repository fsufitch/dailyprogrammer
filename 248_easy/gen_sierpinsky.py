import sys, random

width = int(sys.argv[1])
height = int(sys.argv[2])

print(width, height)

p1 = 0, width//2
p2 = height-1, 0
p3 = height-1, width-1

print("line", 255, 255, 255, *(p1 + p2))
print("line", 255, 255, 255, *(p2 + p3))
print("line", 255, 255, 255, *(p3 + p1))

x, y = height//2, width//2
pts = p1, p2, p3
for i in range(7000):
    px, py = random.choice(pts)
    x = (x + px) // 2
    y = (y + py) // 2
    print("point", 255, 255, 255, x, y)
