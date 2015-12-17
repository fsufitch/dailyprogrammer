package main

// Encode using Huffman coding

import (
	"container/heap"
	"fmt" 
	"io/ioutil"
	"os"
	"unicode"
)

type HuffmanNode struct {
	weight int
	char rune // only set on leaves
	left, right *HuffmanNode
	ggg string
}

func (hn *HuffmanNode) getLeaves() []*HuffmanNode {
	if hn.char > 0 { 
		hn.ggg = ""
		return []*HuffmanNode{hn}
	}
	leaves := []*HuffmanNode{}
	for _, leaf := range hn.left.getLeaves() {
		leaf.ggg = "g" + leaf.ggg
		leaves = append(leaves, leaf)
	}
	for _, leaf := range hn.right.getLeaves() {
		leaf.ggg = "G" + leaf.ggg
		leaves = append(leaves, leaf)
	}
	return leaves
}

type HuffmanNodeHeap []*HuffmanNode

func (h HuffmanNodeHeap) Len() int { return len(h) }
func (h HuffmanNodeHeap) Less(i, j int) bool { return h[i].weight < h[j].weight }
func (h HuffmanNodeHeap) Swap(i, j int) { h[i], h[j] = h[j], h[i] }
func (h *HuffmanNodeHeap) Push(el interface{}) { *h = append(*h, el.(*HuffmanNode)) }
func (h *HuffmanNodeHeap) Pop() (result interface{}) {
	result = (*h)[len(*h)-1]
	*h = (*h)[0:len(*h)-1]
	return
}

func createEncodeMap(message string) (encodeMap map[rune]string) {
	charCounts := map[rune]int{}
	for _, char := range(message) {
		if !unicode.IsLetter(char) { continue }
		if _, ex := charCounts[char]; !ex {
			charCounts[char] = 0
		}
		charCounts[char]++
	}

	charHeap := &HuffmanNodeHeap{}
	heap.Init(charHeap)
	for k, v := range charCounts {
		heap.Push(charHeap, &HuffmanNode{v, k, nil, nil, ""})
	}

	for len(*charHeap) > 1 {
		node1 := heap.Pop(charHeap).(*HuffmanNode)
		node2 := heap.Pop(charHeap).(*HuffmanNode)
		newNode := &HuffmanNode{node1.weight + node2.weight, 0, node1, node2, ""}
		heap.Push(charHeap, newNode)
	}

	leaves := heap.Pop(charHeap).(*HuffmanNode).getLeaves()
	encodeMap = map[rune]string{}
	for _, node := range leaves {
		encodeMap[node.char] = node.ggg
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
