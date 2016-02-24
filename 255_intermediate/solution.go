package main

import "fmt"
import "math/big"
import "os"
import "sort"
import "strconv"

type LinkedDigit struct {
	value int
	nextSig *LinkedDigit
}

func convertToDecimal(digit *LinkedDigit, base int) *big.Int {
	if digit == nil { return big.NewInt(0) }
	
	return (&big.Int{}).Add(
		big.NewInt(int64(digit.value)),
		(&big.Int{}).Mul(
			big.NewInt(int64(base)),
			convertToDecimal(digit.nextSig, base)))
}

func iterateNextDigit(input string, base int, digit *LinkedDigit, outputs *[]*big.Int) {
	if len(input) < 1 {
		output := convertToDecimal(digit, base)
		*outputs = append(*outputs, output)
		return
	}

	for bufSize:=1; bufSize<=len(input); bufSize++ {
		if (bufSize > 1) && input[0]=='0' {
			break // 0 padded numbers are not ok
		}
		buf := input[:bufSize]
		digitValue, _ := strconv.Atoi(buf)
		if digitValue >= base {
			break
		}
		iterateNextDigit(input[bufSize:], base, &LinkedDigit{digitValue, digit}, outputs)
	}
}

type SortBigInts []*big.Int

func (x SortBigInts) Len() int { return len(x) }
func (x SortBigInts) Swap(i, j int) { x[i], x[j] = x[j], x[i] }
func (x SortBigInts) Less(i, j int) bool { return x[i].Cmp(x[j]) < 0 }

func main() {
	inputNum := os.Args[1]
	base, _ := strconv.Atoi(os.Args[2])

	outputs := []*big.Int{}
	iterateNextDigit(inputNum, base, nil, &outputs)
	sort.Sort(SortBigInts(outputs))
	
	for i, output := range outputs {
		if (i > 0) && (output.Cmp(outputs[i-1])==0) {
			continue // No repeats!
		}
		fmt.Println(output)
	}
}
