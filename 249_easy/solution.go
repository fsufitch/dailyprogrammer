package main

import "fmt"
import "io/ioutil"
import "os"
import "strconv"
import "strings"

func main() {
	// Storing money as floating point is a bad idea. 
	// tl;dr why: http://stackoverflow.com/a/3730249
	nums := []int{} 
	input, _ := ioutil.ReadAll(os.Stdin)

	for _, strnum := range strings.Fields(string(input)) {
		fpnum, err := strconv.ParseFloat(strnum, 64)
		if err != nil { panic(err) }
		num := int(fpnum * 100 + 0.1) // Terrible conversion to avoid rounding error
		nums = append(nums, num)
	}

	best_start, best_end, start, end := 0, 0, 0, 0
	for end < len(nums) {
		if ( (nums[end]-nums[start]) > (nums[best_end]-nums[best_start]) && (end-start > 1) ) {
			best_start, best_end = start, end
		}
		if nums[end] < nums[start] {
			start = end
		}
		end++
	}

	fmt.Printf("%.2f %.2f\n", float64(nums[best_start])/100.0, float64(nums[best_end])/100.0)
}
