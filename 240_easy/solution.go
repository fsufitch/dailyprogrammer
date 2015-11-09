package main

import ( 
	"fmt"
	"os"
	"io/ioutil"
	"math/rand"
	"regexp"
)

func scramble(word []byte) (output []byte) {
	output = append([]byte{}, word[0])
	if len(word) == 1 { return }
	if len(word) > 2 {
		toScramble := word[1 : len(word)-1]
		scrambleIndices := rand.Perm(len(toScramble))
		scrambled := make([]byte, len(toScramble))
		for i := range scrambled {
			scrambled[i] = toScramble[scrambleIndices[i]]
		}
		output = append(output, scrambled...)
	}
	output = append(output, word[len(word)-1])
	return
}

func main() {
	inputFile := os.Args[1]
	data, err := ioutil.ReadFile(inputFile)
	if err != nil { panic(err) }

	output := []byte{}

	wordFinderRegexp := regexp.MustCompile("((?i)[a-z]+)")
	for len(data) > 0 {
		match := wordFinderRegexp.FindIndex(data)
		if match == nil {
			output = append(output, data...)
			break
		}
		matchStart, matchEnd := match[0], match[1]
		output = append(output, data[:matchStart]...)
		scrambled := scramble(data[matchStart:matchEnd])
		output = append(output, scrambled...)
		data = data[matchEnd:]
	}
	fmt.Println(string(output))
}
