import random

fruits = open('wiki_fruits.txt').readlines()

for fruit in fruits:
    fruit = fruit.strip()
    print(fruit, random.randrange(1, 600))
