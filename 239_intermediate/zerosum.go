package main

import (
	"fmt"
	"os"
	"strconv"
)

type ThreesState struct {
	N uint64
	StepSum int64
}

type ThreesNode struct {
	ThreesState
	PrevNode *ThreesNode
}

func (node *ThreesNode) PrintTrace(nextN uint64) {
	if node == nil { return }
	node.PrevNode.PrintTrace(node.ThreesState.N)
	move := int64((nextN * 3) - node.ThreesState.N)
	fmt.Printf("%d %d\n", node.ThreesState.N, move)
}


func main() {
	N, e := strconv.ParseUint(os.Args[1], 10, 64)
	if e != nil { panic(e) }
	
	startNode := ThreesNode{
		ThreesState: ThreesState{N, 0},
		PrevNode: nil,
	}
	visitedStepNodes := map[ThreesState]*ThreesNode{}
	nodes := []ThreesNode{startNode}

	possibleMoves := map[int][]int{
		0: []int{0},
		1: []int{-1, 2},
		2: []int{1, -2},
	}

	var foundSolutionNode *ThreesNode

	for len(nodes)>0 {
		node := nodes[0]
		nodes = nodes[1:]

		if _, exists := visitedStepNodes[node.ThreesState]; exists {
			continue
		} else {
			visitedStepNodes[node.ThreesState] = &node;
		}
		
		if node.ThreesState.N == 1 {
			if node.ThreesState.StepSum == 0 {
				foundSolutionNode = &node
				break
			}
			continue
		}
		
		rem := int(node.ThreesState.N % 3)
		for _, move := range possibleMoves[rem] {
			nodes = append(nodes, ThreesNode{
				ThreesState: ThreesState{
					(node.ThreesState.N + uint64(move)) / 3,
					node.ThreesState.StepSum + int64(move),
				},
				PrevNode: &node,
			})
		}
	}
	
	if foundSolutionNode == nil {
		fmt.Println("Impossible.")
		os.Exit(0)
	}

	foundSolutionNode.PrevNode.PrintTrace(1)
	fmt.Println("1")
}
