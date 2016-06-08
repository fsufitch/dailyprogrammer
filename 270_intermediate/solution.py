import random, sys

train_file = sys.argv[1]
seed_words = sys.argv[2:]

if len(seed_words) < 2:
    print("moar seed words!")

prefix_map = {} # (word, word) => {word: count}

training_words = open(train_file).read().split()
for i in range(2, len(training_words)):
    w1, w2, w3 = training_words[i-2:i+1]
    w1 = w1.lower()
    w2 = w2.lower()
    if (w1, w2) not in prefix_map:
        prefix_map[w1, w2] = {}
    if w3 not in prefix_map[w1, w2]:
        prefix_map[w1, w2][w3] = 0
    prefix_map[w1, w2][w3] += 1

output = seed_words[:]

for i in range(500):
    w1, w2 = [w.lower() for w in output[-2:]]
    if (w1, w2) not in prefix_map:
        break # oops
    choices = []
    for k,v in prefix_map[w1,w2].items():
        choices += [k] * v
    output.append(random.choice(choices))

print(*output)
