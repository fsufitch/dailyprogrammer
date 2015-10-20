package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func getWords() []string {
	wordsData, err := ioutil.ReadFile(os.Args[1])
	if err != nil { panic(err) }
	lines := strings.Split(string(wordsData), "\n")

	for i := 0; i < len(lines); i++ {
		lines[i] = strings.ToLower(lines[i])
	}
	return lines
	
}

func canSpell(word string, keys []byte) bool {
	for _, byte := range []byte(word) {
		if bytes.IndexByte(keys, byte) < 0 {
			return false;
		}
	}
	return true;
}

func main() {
	words := getWords()
	inputData, err := ioutil.ReadAll(os.Stdin)
	if err != nil { panic(err) }

	inputLines := strings.Split(string(inputData), "\n")[1:]
	for _, keys := range inputLines {
		if len(keys) < 1 {
			continue
		}
		keys = strings.ToLower(keys)
		var longestWord string
		for _, word := range words {
			if canSpell(word, []byte(keys)) && len(word) > len(longestWord) {
				longestWord = word
			}
		}
		fmt.Println(keys, "=", longestWord)
	}
}
