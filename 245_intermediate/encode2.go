package main

// Encode using a bit-based count algorithm

import ("fmt" 
	"io/ioutil"
	"math"
	"os"
	"unicode"
)

func createGggString(mask int, length int) string {
	ggg := ""
	for i:=0; i<length; i++ {
		if mask & 1 == 0 {
			ggg += "g"
		} else {
			ggg += "G"
		}
		mask >>= 1
	}
	return ggg
}

func createEncodeMap(message string) (encodeMap map[rune]string) {
	charSet := map[rune]bool{}
	for _, char := range(message) {
		if unicode.IsLetter(char) {
			charSet[char] = true
		}
	}

	encodeMap = map[rune]string{}
	gggLength := int( math.Log2(float64(len(charSet)) ) ) + 1
	count := 0
	for k, _ := range charSet {
		encodeMap[k] = createGggString(count, gggLength)
		count++
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
