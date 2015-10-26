package main;

import ( 
	"fmt"
	"io/ioutil"
	"math/rand"
	"os"
	"strings"
	"time"
	"unicode"
)

func genLetter(r rune, consonants []rune, vowels []rune) (output string) {
	if unicode.ToLower(r) == 'c' {
		output = string(consonants[rand.Intn(len(consonants))])
	}
	if unicode.ToLower(r) == 'v' {
		output = string(vowels[rand.Intn(len(vowels))])
	}
	if unicode.IsUpper(r) {
		output = strings.ToUpper(output)
	}
	return
}

func main() {
	rand.Seed(time.Now().Unix())

	consonants := []rune("qwrtypsdfghjklzxcvbnm")
	vowels := []rune("aeiouy")

	inputData, err := ioutil.ReadFile(os.Args[1])
	if err != nil { panic(err) }

	lines := strings.Split(string(inputData), "\n")
	for _, line := range lines {
		for _, r := range line {
			fmt.Printf("%s", genLetter(r, consonants, vowels))
		}
		fmt.Println("")
	}
}
