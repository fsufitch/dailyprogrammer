package main

import ("bufio" 
	"fmt" 
	"os"
	"strings"
)

func createDecodeMap(keyLine string) (decodeMap map[string]string) {
	chunks := strings.Fields(keyLine)
	decodeMap = map[string]string{}
	for i,j := 0,1; j < len(chunks); i,j = i+2,j+2 {
		realChar := []rune(chunks[i]) [0]
		gggChar := chunks[j]
		decodeMap[gggChar] = string(realChar)
	}
	return
}

func main() {
	file := os.Stdin
	if len(os.Args) > 1 {
		var err error
		file, err = os.Open(os.Args[1])
		if err != nil { panic(err) }
		defer file.Close()
	}
	
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	scanner.Scan()
	decodeMap := createDecodeMap(scanner.Text())

	scanner.Split(bufio.ScanRunes)
	inputBuffer := []rune{}
	for scanner.Scan() {
		nextChar := []rune(scanner.Text())[0]
		if nextChar == 'G' || nextChar == 'g' {
			inputBuffer = append(inputBuffer, nextChar)
			if decoded, ex := decodeMap[string(inputBuffer)]; ex {
				fmt.Print(decoded)
				inputBuffer = []rune{}
			}
		} else {
			fmt.Print(string(inputBuffer) + scanner.Text())
			inputBuffer = []rune{}
		}
	}
	
}
