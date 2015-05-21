import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Fizz Buzz input for reverse-Fizz-Buzz problem")
    parser.add_argument("max_num", metavar="N", type=int, nargs=1, help="generate Fizz Buzz from 1 to N")
    parser.add_argument("words", metavar="WORD=DIVISOR", type=str, nargs="+", help="words and their divisors in 'word=divisor' format")
    parser.add_argument("-f", "--full", action="store_true", default=False, help="print the full Fizz Buzz output, including numbers")

    args = parser.parse_args()
    max_num = args.max_num[0]
    words_map = {}
    for word_input in args.words:
        if "=" not in word_input:
            raise ValueError("Input '%s' does not contain '='" % word_input)
        word, divisor = word_input.strip().split('=', 1)
        divisor = int(divisor)
        if divisor in words_map:
            raise ValueError("Divisor %s already specified" % divisor)
        if word in words_map.values():
            raise ValueError("Word '%s' already specified" % word)
        words_map[divisor] = word

    #####
    print("%s %s" % (len(words_map), max_num))
        
    for i in range(1, max_num+1):
        words = []
        for count, word in words_map.items():
            if i % count == 0:
                words.append(word)
        if words:
            print(' '.join(words))
        elif args.full:
            print(i)
            

if __name__ == "__main__": main()
