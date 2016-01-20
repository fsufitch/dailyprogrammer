package main

import ("fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
)

//////// Generics
type Pixel struct {
	red, green, blue int
}
type Image [][]Pixel
type Command interface {
	Init(p Pixel, args []string)
	Draw(img *Image)
}

func (img *Image) toPPM(verbose bool) (out string) {
	intFmt := "%d"
	pixelSep := " "
	endLine := " "
	if verbose { 
		intFmt = "%3d" 
		pixelSep = "    "
		endLine = "\n"
	}

	out = "P3" + endLine
	out += fmt.Sprintf("%d %d%s", len((*img)[0]), len(*img), endLine)
	out += "255" + endLine
	for _, row := range(*img) {
		rowFmtChunks := make([]string, len(row))
		fmtArgs := make([]interface{}, len(row))
		for i, val := range(row) {
			rowFmtChunks[i] = "%s"
			fmtArgs[i] = fmt.Sprintf(intFmt + " " + intFmt + " " + intFmt, 
				val.red, val.green, val.blue)
		}
		rowFmt := strings.Join(rowFmtChunks, pixelSep) + endLine
		out += fmt.Sprintf(rowFmt, fmtArgs...)
	}
	return
}

//////// Points
type DrawPoint struct {
	p Pixel
	row, col int
}
func (cmd *DrawPoint) Init(p Pixel, args []string) {
	cmd.p = p
	cmd.row, _ = strconv.Atoi(args[0])
	cmd.col, _ = strconv.Atoi(args[1])
}
func (cmd *DrawPoint) Draw(img *Image) {
	(*img)[cmd.row][cmd.col] = cmd.p
}

//////// Rects
type DrawRect struct {
	p Pixel
	row, col, height, width int
}
func (cmd *DrawRect) Init(p Pixel, args []string) {
	cmd.p = p
	cmd.row, _ = strconv.Atoi(args[0])
	cmd.col, _ = strconv.Atoi(args[1])
	cmd.height, _ = strconv.Atoi(args[2])
	cmd.width, _ = strconv.Atoi(args[3])
}
func (cmd *DrawRect) Draw(img *Image) {
	for dr:=0; dr<cmd.height; dr++ {
		for dc:=0; dc<cmd.width; dc++ {
			(*img)[cmd.row+dr][cmd.col+dc] = cmd.p
		}
	}
}

//////// Lines
type DrawLine struct {
	p Pixel
	row1, col1, row2, col2 int
}
func (cmd *DrawLine) Init(p Pixel, args []string) {
	cmd.p = p
	cmd.row1, _ = strconv.Atoi(args[0])
	cmd.col1, _ = strconv.Atoi(args[1])
	cmd.row2, _ = strconv.Atoi(args[2])
	cmd.col2, _ = strconv.Atoi(args[3])
}
func (cmd *DrawLine) Draw(img *Image) {
	drow := cmd.row2 - cmd.row1
	dcol := cmd.col2 - cmd.col1

	rowInc := 1
	if drow < 0 { rowInc = -1 }
	colInc := 1
	if dcol < 0 { colInc = -1 }

	if drow == 0 { // Special case
		for col:=cmd.col1; col!=cmd.col2; col+=colInc {
			(*img)[cmd.row1][col] = cmd.p
		}
		return
	}
	
	slope := float64(dcol) / float64(drow)
	currCol := cmd.col1
	for row:=cmd.row1; row!=cmd.row2; row+=rowInc {
		(*img)[row][currCol] = cmd.p
		
		exactCol := slope * float64(row - cmd.row1) + float64(cmd.col1)
		if math.Abs(exactCol - float64(currCol)) < 0.5 {
			currCol += colInc
		}
		for math.Abs(exactCol - float64(currCol)) < 0.5 {
			(*img)[row][currCol] = cmd.p
			currCol += colInc
		}
	}
	(*img)[cmd.row2][cmd.col2] = cmd.p
}


//////// Main stuff

func createCommand(inputs []string, cursor *int) Command {
	cmdName := inputs[*cursor]
	red, _ := strconv.Atoi(inputs[*cursor+1])
	green, _ := strconv.Atoi(inputs[*cursor+2])
	blue, _ := strconv.Atoi(inputs[*cursor+3])
	pixel := Pixel{red, green, blue}

	switch cmdName {
	case "point":
		cmd := &DrawPoint{}
		cmd.Init(pixel, inputs[*cursor+4:*cursor+6])
		*cursor += 6
		return cmd
	case "rect":
		cmd := &DrawRect{}
		cmd.Init(pixel, inputs[*cursor+4:*cursor+8])
		*cursor += 8
		return cmd
	case "line":
		cmd := &DrawLine{}
		cmd.Init(pixel, inputs[*cursor+4:*cursor+8])
		*cursor += 8
		return cmd
	}
	panic("No such command: "+cmdName)
}
		
func main() {
	inputData, err := ioutil.ReadFile(os.Args[1])
	if (err != nil) { panic(err) }
	inputs := strings.Fields(string(inputData))

	cols, _ := strconv.Atoi(inputs[0])
	rows, _ := strconv.Atoi(inputs[1])

	img := Image{}
	for i:=0; i<rows; i++ {
		emptyRow := make([]Pixel, cols)
		img = append(img, emptyRow)
	}

	cursor := 2
	for cursor < len(inputs) {
		cmd := createCommand(inputs, &cursor)
		cmd.Draw(&img)
	}

	fmt.Print(img.toPPM(false))
}
