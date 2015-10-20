package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"os"
	"strconv"
)

// Struct to contain damage about an upcoming damage hit
type DamageNode struct {
	damage int         // amount of damage to do
	time int           // time at which to do it (use this for heap ordering)
	isBoss bool        // damage is from the boss
	timeIncrement int  // time to increment for the next hit
}

type DamageHeap []DamageNode

// Implementation of heap.Interface for DamageHeap
func (h DamageHeap) Len() int { return len(h) }
func (h DamageHeap) Less(index1, index2 int) bool { 
	if h[index1].time == h[index2].time {
		return h[index1].isBoss
	} else {
		return h[index1].time < h[index2].time
	}
}
func (h DamageHeap) Swap(index1, index2 int) { h[index1], h[index2] = h[index2], h[index1] }
func (h *DamageHeap) Push(node interface{}) {
	// add element to the end of the heap, asserting type as DamageNode
	*h = append(*h, node.(DamageNode)) 
}
func (h *DamageHeap) Pop() interface{} {
	// Pop the last element off
	el := (*h)[len(*h)-1]
	*h = (*h)[0:len(*h)-1]
	return el
}

func consumeInput() (damageQueue *DamageHeap, leeroyHP int, bossHP int) {
	f, err := os.Open(os.Args[1])
	if err != nil { panic(err) }

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanWords)
	
	scanner.Scan()
	leeroyHP, err = strconv.Atoi(scanner.Text())
	if err != nil { panic(err) }

	scanner.Scan()
	bossHP, err = strconv.Atoi(scanner.Text())
	if err != nil { panic(err) }

	scanner.Scan()
	bossDamage, err := strconv.Atoi(scanner.Text())
	if err != nil { panic(err) }

	scanner.Scan()
	bossInterval, err := strconv.Atoi(scanner.Text())
	if err != nil { panic(err) }

	damageQueue = &DamageHeap{}
	heap.Push( damageQueue, DamageNode{
		damage: bossDamage,
		time: 0,
		isBoss: true,
		timeIncrement: bossInterval} )
	
	for scanner.Scan() {
		playerDamage, err := strconv.Atoi(scanner.Text())
		if err != nil { panic(err) }
		
		scanner.Scan()
		playerInterval, err := strconv.Atoi(scanner.Text())
		if err != nil { panic(err) }

		heap.Push( damageQueue, DamageNode{
			damage: playerDamage,
			time: 0,
			isBoss: false,
			timeIncrement: playerInterval} )
	}
	return
}

func main() {
	damageQueue, leeroyHP, bossHP := consumeInput()
	
	for leeroyHP > 0 && bossHP > 0 {
		damageNode := heap.Pop(damageQueue).(DamageNode)
		if damageNode.isBoss {
			leeroyHP -= damageNode.damage
		} else {
			bossHP -= damageNode.damage
		}
		damageNode.time += damageNode.timeIncrement
		heap.Push(damageQueue, damageNode)
	}

	if leeroyHP < 1 {
		fmt.Println("Leeroy died.")
	} else {
		fmt.Printf("Leeroy survived with %d HP!\n", leeroyHP)
	}
}
