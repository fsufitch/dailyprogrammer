import argparse, functools, random, sys

A_TO_Z = [chr(x) for x in range(ord('a'), ord('z')+1)]

class DictionaryTree(object):
    def __init__(self, words):
        self.tree = {}
        for word in words:
            self.add_word(word)

    def add_word(self, word):
        node = self.tree
        for char in word.lower():
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = True # Sentinel for end of word
    
    def __contains__(self, word):
        if not word.isalpha():
            return False
        node = self.tree
        for char in word.lower():
            if char not in node:
                return False
            node = node[char]
        return node.get('#')

    def fix(self, word, word_i=0, startnode=None, numerrors=0, maxerrors=1):
        node = startnode or self.tree
        word = word.lower()
        if word_i == len(word):
            if node.get('#'):
                return [''] # Success!
            return None # Failure!

        char = word[word_i]

        if char in node: # Correct letter spelling
            fixed = self.fix(word, word_i+1, node[char], numerrors, maxerrors)
            if fixed is not None:
                return [char + result for result in fixed]

        if numerrors + 1 > maxerrors: # Nope, too many errors
            return None
        
        results = []
        for correct_char in node:
            if correct_char == '#':
                continue
            fixed = self.fix(word, word_i+1, node[correct_char], numerrors+1, maxerrors)
            if fixed is None:
                continue
            results += [correct_char + result for result in fixed]
        if results:
            return results
        return None

    @functools.lru_cache(maxsize=32768)
    def is_unique_misspellable(self, word):
        """ If at least one letter can be changed such that there is only one fix for the word """
        for i in range(len(word)):
            misspell = None
            for letter in A_TO_Z:
                misspell = word[:i] + letter + word[i+1:]
                if misspell not in self:
                    break
            else:
                continue # No misspellings for the word (?!?)
            fixes = self.fix(misspell)
            if len(fixes)==1 and fixes[0] == word:
                return misspell
        return False

    
    @functools.lru_cache(maxsize=32768)
    def misspell_fixably(self, word):
        possible_misspells = set()
        for i in range(0, len(word)):
            for letter in A_TO_Z:
                misspell = word[:i] + letter + word[i+1:]
                fixed = self.fix(misspell)
                if (misspell not in self
                    and fixed is not None
                    and len(fixed)==1
                    and fixed[0]==word):
                    possible_misspells.add(misspell)
        return possible_misspells

    def garble_tribit(self, word, tribit):
        misspells = self.misspell_fixably(word)
        possible_garbles = []
        
        for i in range(0, len(word)):
            letter = word[i]
            garble_up = chr(ord(letter) + tribit)
            garble_down = chr(ord(letter) - tribit)
            garble = garble_up if garble_up.isalpha() else garble_down
            garbled_word = word[:i] + garble + word[i+1:]
            if garbled_word in misspells:
                possible_garbles.append(garbled_word)
            
        return random.choice(possible_garbles) if possible_garbles else None
        
    @functools.lru_cache(maxsize=32768)
    def supports_all_tribits(self, word):
        for tribit in range(1, 0b111+1):
            if not self.garble_tribit(word, tribit):
                return False
        return True

def to_tribits(s):
    tribits= []
    for char in s:
        tribits.append((ord(char) >> 6 & 7) + 1)
        tribits.append((ord(char) >> 3 & 7) + 1)
        tribits.append((ord(char) >> 0 & 7) + 1)
    return tribits

def from_tribits(tribits):
    chars = []
    trios = [(tribits[i], tribits[i+1], tribits[i+2]) 
             for i in range(0, len(tribits), 3)]
    for trio in trios:
        tb1, tb2, tb3 = trio
        charcode = (tb1-1) << 6 | (tb2-1) << 3 | (tb3-1)
        chars.append(chr(charcode))
    return ''.join(chars)

def word_finder(text, dict_tree=None):
    word_start = None
    for cursor in range(len(text)):
        if (word_start is None) and (text[cursor].isalpha()): # start of a word
            word_start = cursor
        elif (word_start is not None) and not (text[cursor].isalpha() or text[cursor]=="'"): # end of a word
            word = text[word_start:cursor].lower()
            if (not dict_tree) or (word in dict_tree):
                yield word_start, word
            word_start = None
    if word_start:
        word = text[word_start:].lower()
        if (not dict_tree) or (word in dict_tree):
            yield word_start, word

############# ENCODING CODE #################

def fix_container(container, dict_tree):
    """ There should be no misspelled words with a single correction in the container! """
    words_container = list(word_finder(container))
    fixed_container = container[:]
    for word_start, word in words_container:
        #print(word, "in dict_tree:", word in dict_tree)
        if word in dict_tree:
            continue
        fixes = dict_tree.fix(word)
        if not fixes or len(fixes) != 1:
            continue
        fixed_container = fixed_container[:word_start] + fixes[0] + fixed_container[word_start+len(word):]
    return fixed_container

def garble_message(container, message, dict_tree):
    words_container = filter(lambda w: dict_tree.supports_all_tribits(w[1]),
                             word_finder(container, dict_tree))
    words_container = list(words_container)
    tb_message = to_tribits(message)

    if len(tb_message) > len(words_container):
        raise Exception("Not enough garble-able words (%s)! Use a bigger container or smaller message." % len(words_container) )

    misspell_mask = [True] * len(tb_message) + [False] * (len(words_container)-len(tb_message))
    random.shuffle(misspell_mask)

    hb_list = list(reversed(tb_message))
    garbled_container = container[:]

    for i in range(len(words_container)):
        if not misspell_mask[i]:
            continue # This word is not getting garbled
        tribit = hb_list.pop()
        word_start, word = words_container[i]
        word_end = word_start + len(word)
        possible_misspells = dict_tree.misspell_fixably(word)

        new_word = dict_tree.garble_tribit(word, tribit)
        #print(word, '~>', new_word, tribit)

        garbled_container = garbled_container[:word_start] + new_word + garbled_container[word_end:]
    return garbled_container

############# DECODING CODE #################

def diff_letters(word1, word2):
    assert len(word1) == len(word2)
    diffs = []
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            diffs.append( (i, word1[i], word2[i]) )
    return diffs

def ungarble_message(text, dict_tree):
    words_container = filter(lambda w: w[1].isalpha(),
                             word_finder(text))
    fixed_text = text[:]
    tribits = []
    for word_start, word in words_container:
        if word in dict_tree:
            continue # word spelled correctly, nothing to do

        fixed_words = dict_tree.fix(word)
        if (not fixed_words) or (len(fixed_words) > 1) :
            continue # word super misspelled, don't worry about it

        fixed_word = fixed_words[0]
        fixed_text = text[:word_start] + fixed_word + text[word_start+len(word):]

        #print(word, word in dict_tree, fixed_word, fixed_word in dict_tree)
        
        diff = diff_letters(word, fixed_word)
        index, char1, char2 = diff[0]

        tribit = abs(ord(char1) - ord(char2))
        tribits.append(tribit)

    #print(tribits)
    #print(fixed_text)
    message = from_tribits(tribits)
    return message

############# MAIN RUN CODE ###############

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['encode', 'decode'])
    parser.add_argument('text', metavar="TXT_FILE",
                        help="file to be used as a carrier (for encoding) or as a source (for decoding)")
    parser.add_argument('-w', '--words', metavar="WORDS_TXT", default="/usr/share/dict/words",
                        help="path to words/dictionary file to use (default: /usr/share/dict/words)")

    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument('-m', '--message', metavar="MESSAGE", default=None,
                        help="use a text message instead of STDIN for encoding data")
    source_group.add_argument('-f', '--file', metavar="MESSAGE_TXT", default=None,
                              help="use a file instead of STDIN for encoding data")
    
    args = parser.parse_args()

    with open(args.text) as f:
        main_data = f.read()

    with open(args.words) as f:
        words = f.read().split()
    dt = DictionaryTree(words)

    if args.action == 'encode':
        encode_data = args.message
        if args.file:
            with open(args.file) as f:
                encode_data = f.read()
        if not encode_data:
            encode_data = sys.stdin.read()
        
        container = fix_container(main_data, dt)
        encoded = garble_message(container, encode_data, dt)
        sys.stdout.write(encoded)
        sys.stdout.flush()
    else:
        decoded = ungarble_message(main_data, dt)
        print(decoded)

if __name__ == '__main__':
    main()
