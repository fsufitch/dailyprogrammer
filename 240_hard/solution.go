package main

import( "fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

///// Math utils

func permutate(nums []int) (result [][]int) {
	result = [][]int{}
	if len(nums) == 1 {
		return [][]int{ []int{nums[0]} }
	}
 	for i, num := range nums {
		nextNums := append([]int{}, nums[:i]...)
		nextNums = append(nextNums, nums[i+1:]...)
		for _, subPerm := range permutate(nextNums) {
			perm := append([]int{num}, subPerm...)
			result = append(result, perm)
		}
	}
	return result
}

var permCache map[int][][]int
func getPermutations(n int) ([][]int) {
	if _, ex := permCache[n]; !ex {
		nums := []int{}
		for i:=0; i<n; i++ {
			nums = append(nums, i)
		}
		if permCache == nil {
			permCache = map[int][][]int{}
		}
		permCache[n] = permutate(nums)
	}
	return permCache[n]
}

func addTo(result int, nums []int) bool {
	r := 0
	for _, n := range nums {
		r += n
	}
	return r == result
}

func multiplyTo(result int, nums []int) bool {
	r := 1
	for _, n := range nums {
		r *= n
	}
	return r == result
}

func subtractTo(result int, nums []int) bool {
	for _, order := range getPermutations(len(nums)) {
		r := nums[order[0]]
		for i:=1; i<len(nums); i++ {
			n := nums[order[i]]
			r -= n
		}
		if r == result {
			return true
		}
	}
	return false
}

func divideTo(result int, nums []int) bool {
	for _, order := range getPermutations(len(nums)) {
		r := nums[order[0]]
		divisionFailed := false
		for i:=1; i<len(nums); i++ {
			n := nums[order[i]]
			if r % n > 0 {
				divisionFailed = true
				break
			}
			r /= n
		}
		if !divisionFailed && r == result {
			return true
		}
	}
	return false
}

func equalsTo(result int, nums []int) bool {
	return len(nums)==1 && nums[0]==result
}

///// Coordinates

type Coordinate struct {
	Row, Col int
	Text string
}

func CoordinateFromString(input string) (coord Coordinate) {
	coord = Coordinate{Text: input}
	row, err := strconv.Atoi(input[1:])
	if (err != nil) { panic(err) }
	coord.Row = row - 1
	coord.Col = int(input[0]) - 65
	return
}

///// Generic constraint interface


type Constraint interface {
	CanEvaluate(map[Coordinate]int) bool // Can evaluate a constraint when all required inputs are bound
	Evaluate(map[Coordinate]int) bool // Evaluate to whether the constraint is satisfied or not
}

///// Constraint for KenKen calculation rules

type KenKenConstraint struct {
	Result int
	Operation rune
	Inputs []Coordinate
}

func KenKenConstraintFromLine(line string) (c *KenKenConstraint) {
	chunks := strings.Fields(line)
	if len(chunks) < 3 {
		return nil
	}

	result, err := strconv.Atoi(chunks[0])
	if (err != nil) { panic(err) }

	c = &KenKenConstraint{}
	c.Result = result
	c.Operation = rune(chunks[1][0])
	c.Inputs = []Coordinate{}
	for _, coordString := range chunks[2:] {
		c.Inputs = append(c.Inputs, CoordinateFromString(coordString))
	}
	return
}


func (c KenKenConstraint) CanEvaluate(values map[Coordinate]int) bool {
	for _, input := range c.Inputs {
		if _, ex := values[input]; !ex {
			return false
		}
	}
	return true
}

func (c KenKenConstraint) Evaluate(values map[Coordinate]int) bool {
	if !(c.CanEvaluate(values)) { return false }
	
	expectedResult := c.Result
	inputValues := []int{}
	for _, coord := range c.Inputs {
		inputValues = append(inputValues, values[coord])
	}

	switch c.Operation {
	case '+': 
		return addTo(expectedResult, inputValues)
	case '-':
		return subtractTo(expectedResult, inputValues)
	case '*':
		return multiplyTo(expectedResult, inputValues)
	case '/':
		return divideTo(expectedResult, inputValues)
	case '=':
		return equalsTo(expectedResult, inputValues)
	default:
		panic(fmt.Sprintf("%s is not a valid operation!", c.Operation))
	}
}

///// Constraint for row/column uniqueness

type LineUniqueConstraint struct {
	Min, Max int
	Members []Coordinate
}

func (c LineUniqueConstraint) CanEvaluate(values map[Coordinate]int) bool {
	return true
}

func (c LineUniqueConstraint) Evaluate(values map[Coordinate]int) bool {
	if !(c.CanEvaluate(values)) { return false }

	valuesSeen := map[int]bool{}
	for _, coord := range c.Members {
		if _, ex := values[coord]; !ex {
			continue // Don't worry about missing values
		}
		if values[coord] < c.Min || values[coord] > c.Max || valuesSeen[values[coord]] {
			return false // Saw same value twice, or value is outside proper range
		}
		valuesSeen[values[coord]] = true
	}
	return true
}

///// Solution + utils

func copySolution(solution map[Coordinate]int) (newSolution map[Coordinate]int) {
	newSolution = map[Coordinate]int{}
	for k,v := range solution {
		newSolution[k] = v
	}
	return
}

func printSolution(gridSize int, solution map[Coordinate]int) {
	for r:=0; r<gridSize; r++ {
		for c:=0; c<gridSize; c++ {
			coordString := fmt.Sprintf("%s%d", string(rune(65+c)), r+1)
			coord := CoordinateFromString(coordString)
			var out string
			out = fmt.Sprint(solution[coord])
			if _, ex := solution[coord]; !ex {
				out = "_"
			}
			fmt.Printf("%s ", out)
		}
		fmt.Println("")
	}
}

func solve(coords []Coordinate, constraints []Constraint, domain []int) (*map[Coordinate]int) {
	solutions := []map[Coordinate]int{ map[Coordinate]int{} }
	
	for _, c := range coords {
		nextSolutions := []map[Coordinate]int{}
		for _, solution := range solutions {
			solution = copySolution(solution)
			//printSolution(len(domain), solution)
			for _, value := range domain {
				solution[c] = value
				useSolution := true
				//fmt.Printf("Solution eval: %s\n", fmt.Sprint(solution))

				for _, constraint := range constraints {
					//fmt.Printf("  Constraint Eval: %s\n", fmt.Sprint(constraint))
					if constraint.CanEvaluate(solution) && !constraint.Evaluate(solution) {
						//fmt.Printf("    [%d] Bad! %s |||| %s\n", value, fmt.Sprint(solution), fmt.Sprint(constraint))
						useSolution = false
						break
					}
				}
				if useSolution {
					//fmt.Printf("Solution good! [%d]\n", value)
					nextSolutions = append(nextSolutions, copySolution(solution))
				}
			}
		}
		solutions = nextSolutions
	}

	for _, solution := range solutions {
		solutionVerified := true
		for _, constraint := range constraints {
			if constraint.CanEvaluate(solution) && !constraint.Evaluate(solution) {
				solutionVerified = false
				break
			}
		}
		if solutionVerified {
			return &solution
		}
		
	}
	
	return nil
}



///// Main

func CreateGridAndConstraints(gridSize int) ([][]Coordinate, []LineUniqueConstraint) {
	grid := [][]Coordinate{}
	constraints := []LineUniqueConstraint{}
	colLines := map[int][]Coordinate{}

	for row:=0; row<gridSize; row++ {
		rowLine := []Coordinate{}
		for col:=0; col<gridSize; col++ {
			coordString := fmt.Sprintf("%s%d", string(rune(65+col)), row+1)
			coord := CoordinateFromString(coordString)
			rowLine = append(rowLine, coord)

			if _, ex := colLines[col]; !ex {
				colLines[col] = []Coordinate{} // Create the column line if it doesn't exist
			}
			colLines[col] = append(colLines[col], coord)
		}
		grid = append(grid, rowLine)
		constraints = append(constraints, LineUniqueConstraint{1, gridSize+1, rowLine})
	}
	
	for _, colLine := range colLines {
		constraints = append(constraints, LineUniqueConstraint{1, gridSize+1, colLine})
	}
	return grid, constraints
}

func main() {
	fileData, err := ioutil.ReadFile(os.Args[1])
	if (err != nil) { panic(err) }
	
	fileLines := strings.Split(string(fileData), "\n")
	gridSize, err := strconv.Atoi(fileLines[0])
	if (err != nil) { panic(err) }

	coordGrid, gridConstraints := CreateGridAndConstraints(gridSize)

	coords := []Coordinate{}
	for _, row := range coordGrid {
		coords = append(coords, row...)
	}

	domain := []int{}
	for i:=0; i<gridSize; i++ {
		domain = append(domain, i+1)
	}

	constraints := []Constraint{}
	for _, c := range gridConstraints {
		constraints = append(constraints, c)
	}
	
	for _, line := range fileLines[1:] {
		kkc := KenKenConstraintFromLine(line)
		if kkc != nil {
			constraints = append(constraints, kkc)
		}
	}

	solution := solve(coords, constraints, domain)

	if solution == nil {
		fmt.Println("No solution!")
		return
	}

	printSolution(gridSize, *solution)
}
