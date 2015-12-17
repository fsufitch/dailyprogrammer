package main

// Encode using a naive g-count algorithm

import ("fmt" 
	"io/ioutil"
	"os"
	"unicode"
)

func createEncodeMap(message string) (encodeMap map[rune]string) {
	encodeMap = map[rune]string{}
	currentGgg := ""
	for _, char := range(message) {
		if _, ex := encodeMap[char]; !ex && unicode.IsLetter(char) {
			encodeMap[char] = currentGgg + "G"
			currentGgg += "g"
		}
	}
	return
}

func encode(message string, encodeMap map[rune]string) string{
	outputMessage := ""
	for _, char := range(message) {
		encoded, ex := encodeMap[char]
		if !ex { encoded = string(char) }
		outputMessage += encoded
	}
	return outputMessage
}

func main() {
	file := os.Stdin
	if len(os.Args) > 1 {
		var err error
		file, err = os.Open(os.Args[1])
		if err != nil { panic(err) }
		defer file.Close()
	}

	message, err := ioutil.ReadAll(file)
	if err != nil { panic(err) }

	encodeMap := createEncodeMap(string(message))
	for k, v := range encodeMap {
		fmt.Printf("%s %s ", string(k), v)
	}
	fmt.Println()

	output := encode(string(message), encodeMap)
	fmt.Print(output)
}
