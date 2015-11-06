package main

import (
	"fmt"
	"math"
	"math/big"
	//"io/ioutil"
	"os"
	//"strings"
	//"unicode"
)
/*
type WordTrieNode struct {
	EndOfWord bool
	NextNodes map[rune]*WordTrieNode
}

func (n *WordTrieNode) IsWord(chars []rune) bool {
	if len(chars) == 0 {
		return n.EndOfWord
	}
	currChar := unicode.ToLower(chars[0])
	if nextNode, ex := n.NextNodes[currChar]; ex {
		return nextNode.IsWord(chars[1:])
	}
	return false
}

func (n *WordTrieNode) IsPartWord(chars []rune) bool {
	if len(chars) == 0 {
		return true
	}
	currChar := unicode.ToLower(chars[0])
	if nextNode, ex := n.NextNodes[currChar]; ex {
		return nextNode.IsPartWord(chars[1:])
	}
	return false
}

func (n *WordTrieNode) AddWord(chars []rune) {
	if len(chars) == 0 {
		n.EndOfWord = true
	} else {
		currChar := chars[0] // unicode.ToLower(chars[0])
		if _, ex := n.NextNodes[currChar]; !ex {
			n.NextNodes[currChar] = &WordTrieNode{false, map[rune]*WordTrieNode{}}
		}
		n.NextNodes[currChar].AddWord(chars[1:])
	}
}

func (n *WordTrieNode) LoadFile(fname string) {
	fileData, err := ioutil.ReadFile(fname)
	if (err != nil) { panic(err) }

	lines := strings.Split(string(fileData), "\n")
	for _, line := range lines {
		line = strings.TrimSpace(line)
		n.AddWord([]rune(line))
	}
}

*/

// ===============

func TernaryToInt(ternBits []int) (r int) {
	r = 0
	for i:=len(ternBits)-1; i>=0; i-- {
		pow := len(ternBits)-1-i
		r += ternBits[i] * int(math.Pow(3, float64(pow)))
	}
	return
}

// ===============

type TraverseState struct {
	chars []rune
	N *big.Int
	TernaryBuffer []int
	debugMoves []int
}


func verifyStep(originalN *big.Int, moves []int, nowN *big.Int) {
	n := big.NewInt(0).Add(big.NewInt(0), originalN)
	output := ""
	for _, move := range moves {
		oldN := big.NewInt(0).Add(big.NewInt(0), n)
		
		newN := big.NewInt(0).Add(big.NewInt(0), n)
		newN = newN.Add(newN, big.NewInt(int64(move)))
		newN = newN.Div(newN, big.NewInt(3))
		
		output += fmt.Sprintf("(%s + %d) / 3 == %s\n", oldN.String(), move, newN.String())
		
		n = newN
	}
	if n.Cmp(nowN) != 0 {
		output += fmt.Sprintf("XXXXXX: %s != %s\n", n.String(), nowN.String())
		fmt.Println(output)
	}
}

func decodeThrees(/*wordTrie *WordTrieNode,*/ N *big.Int) (solutions []string) {
	states := []TraverseState{
		TraverseState{[]rune{}, N, []int{}, []int{}},
	}
	possibleMoves := map[int][]int{
		0: []int{0},
		1: []int{-1, 2},
		2: []int{1, -2},
	}

	solutions = []string{}

	for len(states) > 0 {
		currState := states[0]
		states = states[1:]

		if currState.N.Cmp(big.NewInt(0)) == 0 {
			continue
		}
		
		//verifyStep(N, currState.debugMoves, currState.N)
			
		if currState.N.Cmp(big.NewInt(1)) == 0 {
			if /*wordTrie.IsWord(currState.chars) &&*/ len(currState.TernaryBuffer) == 0 {
				//fmt.Println(string(currState.chars), currState.debugMoves)
				solutions = append(solutions, string(currState.chars))
			}
			continue
		}
		
		remainder := int(big.NewInt(0).Mod(currState.N, big.NewInt(3)).Int64())
		moves := possibleMoves[remainder]
		
		for _, move := range moves {
			if move == 0 && len(currState.TernaryBuffer) == 0 {
				continue // Edge case, causing 0-buffering problems
			}

			newTernaryBuffer := append([]int{}, currState.TernaryBuffer...)
			newTernaryBuffer = append(newTernaryBuffer, int(math.Abs(float64(move))))

			newDebugMoves := append([]int{}, currState.debugMoves...)
			newDebugMoves = append(newDebugMoves, move)

			newN := big.NewInt(0).Add(big.NewInt(0), currState.N)
			newN = newN.Add(newN, big.NewInt(int64(move)))
			newN = newN.Div(newN, big.NewInt(3))

			//fmt.Println("   (", currState.N, "+", move, ") // 3 ==", newN)
			
			if TernaryToInt(newTernaryBuffer) > 255 {
				continue // Next move if this buffer is not sane
			}
			
			// Try to simply append to the buffer
			//fmt.Println("       X ", TraverseState{currState.chars, newN, newTernaryBuffer})
			states = append(states, TraverseState{currState.chars, newN, newTernaryBuffer, newDebugMoves})
			
			// Try to make a new letter
			newChars := append([]rune{}, currState.chars...)
			newChars = append(newChars, rune(TernaryToInt(newTernaryBuffer)))
			//fmt.Printf("      + %d -> %d -> %s (%s)\n", move, TernaryToInt(newTernaryBuffer), string(rune(TernaryToInt(newTernaryBuffer))), fmt.Sprint(newTernaryBuffer))
			

			//if wordTrie.IsPartWord(newChars) {
			char_val := TernaryToInt(newTernaryBuffer)
			if (char_val>=33 && char_val <=126) {
				//fmt.Println("       O ", TraverseState{newChars, newN, []int{}})
				states = append(states, TraverseState{newChars, newN, []int{}, newDebugMoves})
			}
		}
	}
	
	return
}


func main() {
	/*
	wordPath := os.Args[1]

	wordTrie := &WordTrieNode{false, map[rune]*WordTrieNode{}}
	wordTrie.LoadFile(wordPath)
*/

	inputN := big.NewInt(0)
	inputN.SetString(os.Args[1], 10)
	
	solutions := decodeThrees(/*wordTrie,*/ inputN)

	fmt.Println(inputN.String())
	for _, solution := range solutions {
		fmt.Println(solution)
	}
}
