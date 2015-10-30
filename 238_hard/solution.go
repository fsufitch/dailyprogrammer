package main

import (
	"container/heap"
	"fmt"
	"io/ioutil"
	"math"
	"os"
)

/* ===== Core Dungeon Code ===== */

type Dungeon struct {
	FloorMap [][][]byte
	StartFloor, StartRow, StartCol int
	EndFloor, EndRow, EndCol int
}

func NewDungeon(inputBytes []byte) (d Dungeon) {
	d.FloorMap = [][][]byte {}
	currentRow := []byte {}
	currentFloor := [][]byte {}

	for _, b := range inputBytes {
		switch b {
		case '\n':
			if len(currentRow) == 0 {
				// two newlines, end of floor
				d.FloorMap = append(d.FloorMap, currentFloor)
				currentFloor = [][]byte {}
			} else {
				// end of row
				currentFloor = append(currentFloor, currentRow)
				currentRow = []byte {}
			}
		case '#', ' ', 'D', 'U': // regular square
			currentRow = append(currentRow, b)
		case 'S': // start
			d.StartFloor = len(d.FloorMap)
			d.StartRow = len(currentFloor)
			d.StartCol = len(currentRow)
			currentRow = append(currentRow, b)
		case 'G': // end
			d.EndFloor = len(d.FloorMap)
			d.EndRow = len(currentFloor)
			d.EndCol = len(currentRow)
			currentRow = append(currentRow, b)
		} 
	}
	if len(currentRow) > 0 {
		currentFloor = append(currentFloor, currentRow)
	}
	if len(currentFloor) > 0 {
		d.FloorMap = append(d.FloorMap, currentFloor)
	}

	return
}

func (d *Dungeon) IsWithinBounds(floor int, row int, col int) bool {
	return (floor >= 0 && floor < len(d.FloorMap) &&
		row >= 0 && row < len(d.FloorMap[floor]) &&
		col >= 0 && col < len(d.FloorMap[floor][row]))
}

func (d *Dungeon) IsClear(floor int, row int, col int) bool {
	if !d.IsWithinBounds(floor, row, col) { return false }
	switch d.FloorMap[floor][row][col] {
	case '#':
		return false
	}
	return true
}

func (d *Dungeon) CanGoUp(floor int, row int, col int) bool {
	return d.IsWithinBounds(floor, row, col) && (d.FloorMap[floor][row][col] == 'U')
}

func (d *Dungeon) CanGoDown(floor int, row int, col int) bool {
	return d.IsWithinBounds(floor, row, col) && (d.FloorMap[floor][row][col] == 'D')
}

func (d *Dungeon) IsGoal(floor int, row int, col int) bool {
	return (d.EndFloor == floor && d.EndRow == row && d.EndCol == col)
}

func (d *Dungeon) DistanceToGoal(floor int, row int, col int) float64 {
	df := d.EndFloor - floor 
	dr := d.EndRow - row
	dc := d.EndCol - col
	return math.Sqrt(float64(df*df + dr*dr + dc*dc))
}

/* ===== A* Search -- Search Node + Heap ===== */

type SearchNode struct {
	Dungeon *Dungeon
	CurrFloor, CurrRow, CurrCol int
	DistSoFar int
	PrevNode *SearchNode
}

func (n *SearchNode) heuristic() float64 {
	return float64(n.DistSoFar) + n.Dungeon.DistanceToGoal(n.CurrFloor, n.CurrRow, n.CurrCol)
}

func (n *SearchNode) IsBacktracking(tip *SearchNode) bool {
	return ((n.CurrFloor == tip.CurrFloor && n.CurrRow == tip.CurrRow && n.CurrCol == tip.CurrCol) ||
		(n.PrevNode != nil && n.PrevNode.IsBacktracking(tip)))
}

type SearchHeap []*SearchNode 

// === Implements sort/Interface

func (h *SearchHeap) Len() int { return len(*h) }
func (h *SearchHeap) Less(a, b int) bool {
	return (*h)[a].heuristic() < (*h)[b].heuristic()
}
func (h *SearchHeap) Swap(a, b int) {
	(*h)[a], (*h)[b] = (*h)[b], (*h)[a]
}

// === Implements container/heap/Interface
func (h *SearchHeap) Push(el interface{}) {
	node := el.(*SearchNode)
	*h = append(*h, node)
}
func (h *SearchHeap) Pop() interface{} {
	node := (*h)[len(*h)-1]
	*h = (*h) [0 : len(*h)-1]
	return node
}

/* ===== A* Search -- Main Search ===== */

func AStar(dungeon *Dungeon) []*SearchNode {
	nodeHeap := SearchHeap{
		&SearchNode {
			Dungeon: dungeon,
			CurrFloor: dungeon.StartFloor,
			CurrRow: dungeon.StartRow,
			CurrCol: dungeon.StartCol,
			DistSoFar: 0,
			PrevNode: nil,
		},
	}
	heap.Init(&nodeHeap)

	node := &SearchNode{}
	
	for len(nodeHeap) > 0 {
		node = heap.Pop(&nodeHeap).(*SearchNode)
		if node.PrevNode != nil && node.PrevNode.IsBacktracking(node) { continue }

		if dungeon.IsGoal(node.CurrFloor, node.CurrRow, node.CurrCol) {
			break  // Yay!
		}
		
		if dungeon.IsClear(node.CurrFloor, node.CurrRow-1, node.CurrCol) { // Go up
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor, node.CurrRow-1, node.CurrCol, node.DistSoFar+1, node})
		}

		if dungeon.IsClear(node.CurrFloor, node.CurrRow+1, node.CurrCol) { // Go down
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor, node.CurrRow+1, node.CurrCol, node.DistSoFar+1, node})
		}

		if dungeon.IsClear(node.CurrFloor, node.CurrRow, node.CurrCol-1) { // Go left
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor, node.CurrRow, node.CurrCol-1, node.DistSoFar+1, node})
		}

		if dungeon.IsClear(node.CurrFloor, node.CurrRow, node.CurrCol+1) { // Go right
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor, node.CurrRow, node.CurrCol+1, node.DistSoFar+1, node})
		}

		if (dungeon.CanGoDown(node.CurrFloor, node.CurrRow, node.CurrCol) &&
			dungeon.IsClear(node.CurrFloor+1, node.CurrRow, node.CurrCol)) { // Go down a floor
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor+1, node.CurrRow, node.CurrCol, node.DistSoFar+1, node})
		}
			
		if (dungeon.CanGoUp(node.CurrFloor, node.CurrRow, node.CurrCol) &&
			dungeon.IsClear(node.CurrFloor-1, node.CurrRow, node.CurrCol)) { // Go up a floor
			heap.Push(&nodeHeap, &SearchNode{dungeon, node.CurrFloor-1, node.CurrRow, node.CurrCol, node.DistSoFar+1, node})
		}
			
	}

	if len(nodeHeap) == 0 { // Failed :(
		return []*SearchNode{};
	}
	
	solutionNodes := []*SearchNode{node}
	for ; node != nil; node = node.PrevNode {
		solutionNodes = append(solutionNodes, node)
	}
	return solutionNodes;
}

/* ===== Output And Main ===== */

func printDungeonSolution(d Dungeon, solution []*SearchNode) {
	for _, node := range solution {
		//fmt.Printf("%d %d %d\n", node.CurrFloor, node.CurrRow, node.CurrCol)
		currChar := &(d.FloorMap[node.CurrFloor][node.CurrRow][node.CurrCol])
		if *currChar == ' ' {
			*currChar = '*'
		}
	}
	
	for _, floor := range d.FloorMap {
		for _, row := range floor {
			fmt.Printf("%s\n", string(row))
		}
		fmt.Printf("\n")
	}
}

func main() {
	fname := os.Args[1]
	inputBytes, err := ioutil.ReadFile(fname)
	if (err != nil) { panic(err) }

	dungeon := NewDungeon(inputBytes)
	
	solution := AStar(&dungeon)
	if len(solution) == 0 {
		fmt.Println("No path found! :(")
	} else {
		printDungeonSolution(dungeon, solution)
	}
}
