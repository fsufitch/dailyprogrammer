package main

import( "bufio"
	"errors"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
	"unicode"
)

var defaultDay = 24
var defaultMonth = 12
var defaultYear = 2014

type Date [3]int // [Y, M, D]

func (date *Date) isComplete() bool {
	return date[0] > 0 && date[1] > 0 && date[2] > 0
}

func (date *Date) isEmpty() bool {
	return date[0] == 0 && date[1] == 0 && date[2] == 0
}

func (date *Date) plusDays(days int) (result Date) {
	if !date.isComplete() {
		fmt.Println(date)
		panic("Tried to add days to incomplete date")
	}
	realTime := time.Date(date[0], time.Month(date[1]), date[2], 0, 0, 0, 0, time.UTC)
	realTime = realTime.AddDate(0, 0, days)
	result[0] = realTime.Year()
	result[1] = int(realTime.Month())
	result[2] = realTime.Day()
	return
}


// https://groups.google.com/d/msg/golang-nuts/W-ezk71hioo/6qRWMupJoMYJ
func daysIn(m time.Month, year int) int { 
    return time.Date(year, m+1, 0, 0, 0, 0, 0, time.UTC).Day() 
} 

type IncrementType int
const (
	NO_INCREMENT = iota
	DAYS
	WEEKS
	MONTHS
	YEARS
)

var INCREMENTS = map[string]IncrementType {
	"day": DAYS,
	"days": DAYS,
	"week": WEEKS,
	"weeks": WEEKS,
	"month": MONTHS,
	"months": MONTHS,
	"year": YEARS,
	"years": YEARS,
}

var MONTH_NAMES = map[string]time.Month {
	"january": time.January,
	"february": time.February,
	"march": time.March,
	"april": time.April,
	"may": time.May,
	"june": time.June,
	"july": time.July,
	"august": time.August,
	"september": time.September,
	"october": time.October,
	"november": time.November,
	"december": time.December,
	"jan": time.January,
	"feb": time.February,
	"mar": time.March,
	"apr": time.April,
	//"may": time.May,
	"jun": time.June,
	"jul": time.July,
	"aug": time.August,
	"sep": time.September,
	"oct": time.October,
	"nov": time.November,
	"dec": time.December,
}

func monthParseString(month string) time.Month {
	if m, err := strconv.Atoi(month); err == nil { return time.Month(m) }
	month = strings.ToLower(month)
	if m, ex := MONTH_NAMES[month]; ex { return time.Month(m) }
	return time.Month(0)
}

type DateGuess struct {
	date Date
	increment, direction int
	incType IncrementType
	impliedToday bool
}

func (dg *DateGuess) hasIncrement() bool {
	return dg.increment > 0 || dg.direction != 0 || dg.incType != NO_INCREMENT
}

func (dg *DateGuess) hasValidIncrement() bool {
	return dg.increment > 0 && dg.direction != 0 && dg.incType != NO_INCREMENT
}

func (dg *DateGuess) hasInvalidIncrement() bool {
	return dg.hasIncrement() && !dg.hasValidIncrement()
}

func (dg *DateGuess) flatten() (d Date, err error) {
	d = dg.date
	if d.isEmpty() && (!dg.hasIncrement() || dg.impliedToday) {
		d = Date{defaultYear, defaultMonth, defaultDay}
	}
	
	if d[0] < 1 && d[1] > 0 && d[2] > 0 { // year not specified, current year implied
		d[0] = defaultYear
	}

	if !d.isComplete() {
		err = errors.New("guess date is incomplete")
		return
	}

	if d[1] < 1 || d[1] > 12 {
		err = errors.New("bad month")
		return
	}
	if d[2] < 1 || d[2] > daysIn(time.Month(d[1]), d[0]) {
		err = errors.New("bad day")
		return
	}

	if dg.hasIncrement() {
		if dg.hasInvalidIncrement() {
			err = errors.New("invalid increment")
			return
		}
		switch dg.incType {
		case DAYS:
			d = d.plusDays(dg.increment * dg.direction)
		case WEEKS:
			d = d.plusDays(7 * dg.increment * dg.direction)
		case MONTHS:
			newMonths := d[1] + dg.increment * dg.direction
			d[0], d[1] = d[0] + newMonths / 12, newMonths % 12
		case YEARS:
			d[0] += dg.increment * dg.direction
		default:
			err = errors.New("unknown increment type")
			return
		}
	}
	
	return
}

// Guess functions; return a list of "next" guesses when a particular input word is given

func guessIncrementSuffix(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if (strings.ToLower(word) != "from" && 
		strings.ToLower(word) != "after" &&
		strings.ToLower(word) != "hence") { return }
	
	for _, guess := range(guesses) {
		if guess.direction != 0 { continue }
		copyGuess := guess

		if strings.ToLower(word) == "hence" {
			if copyGuess.date.isEmpty() {
				copyGuess.date = Date{defaultYear, defaultMonth, defaultDay}
			} else {
				continue
			}
		}

		copyGuess.direction = 1
		if !copyGuess.hasValidIncrement() { continue }
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessDecrementSuffix(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if (strings.ToLower(word) != "to" && 
		strings.ToLower(word) != "before" &&
		strings.ToLower(word) != "ago") { return }
	
	for _, guess := range(guesses) {
		if guess.direction != 0 { continue }
		copyGuess := guess

		if strings.ToLower(word) == "ago" {
			if copyGuess.date.isEmpty() {
				copyGuess.date = Date{defaultYear, defaultMonth, defaultDay}
			} else {
				continue
			}
		}

		copyGuess.direction = -1
		if !copyGuess.hasValidIncrement() { continue}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessBareNumber(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if _, err := strconv.Atoi(word); err!=nil { return }
	num, _ := strconv.Atoi(word);
	
	for _, guess := range(guesses) {
		copyGuess := guess
		// Crapshoot. Could be anything that isn't already taken.
		
		if (copyGuess.date[0] < 1) {
			copyGuess = guess
			copyGuess.date[0] = num
			nextGuesses = append(nextGuesses, copyGuess)
		}
		if (copyGuess.date[1] < 1) {
			copyGuess = guess
			copyGuess.date[1] = num
			nextGuesses = append(nextGuesses, copyGuess)
		}
		if (copyGuess.date[2] < 1) {
			copyGuess = guess
			copyGuess.date[2] = num
			nextGuesses = append(nextGuesses, copyGuess)
		}
		if (copyGuess.increment < 1) {
			copyGuess = guess
			copyGuess.increment = num
			nextGuesses = append(nextGuesses, copyGuess)
		}
	}
	return
}

func guessBareMonth(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	word = strings.ToLower(word)
	if _, ex := MONTH_NAMES[word]; !ex { return }
	month := MONTH_NAMES[word]
	
	for _, guess := range(guesses) {
		copyGuess := guess
		if copyGuess.date[1] > 0 { continue }
		copyGuess.date[1] = int(month)
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}


func guessIncrementType(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	word = strings.ToLower(word)
	if _, ex := INCREMENTS[word]; !ex { return }
	
	for _, guess := range(guesses) {
		copyGuess := guess
		copyGuess.incType = INCREMENTS[word]
		if (word == "day" || word == "week" || word == "month" || word == "year") && copyGuess.increment < 2 {
			copyGuess.increment = 1
		}

		if copyGuess.increment < 1 { continue }
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessLastNextImplyToday(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	word = strings.ToLower(word)
	if word != "last" && word != "next" { return }
	
	for _, guess := range(guesses) {
		copyGuess := guess
		copyGuess.impliedToday = true
		copyGuess.increment = 1
		copyGuess.direction = 1
		if word == "last" { 
			copyGuess.direction = -1
		}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessTomorrow(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if strings.ToLower(word) != "tomorrow" { return }

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{defaultYear, defaultMonth, defaultDay}
		copyGuess.date = copyGuess.date.plusDays(1)
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessYesterday(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if strings.ToLower(word) != "yesterday" { return }

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{defaultYear, defaultMonth, defaultDay}
		copyGuess.date = copyGuess.date.plusDays(-1)
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessToday(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	nextGuesses = []DateGuess{}
	if strings.ToLower(word) != "today" { return }

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{defaultYear, defaultMonth, defaultDay}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	return
}

func guessYMD(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	re := regexp.MustCompile("([[:digit:]]+)[[:^digit:]]((?:[[:digit:]]|[[:alpha:]])+)[[:^digit:]]([[:digit:]]+)")
	if !re.MatchString(word) { 
		return 
	}

	match := re.FindStringSubmatch(word)
	y, _  := strconv.Atoi(match[1])
	m  := int(monthParseString(match[2]))
	d, _  := strconv.Atoi(match[3])

	nextGuesses = []DateGuess {}

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{y, m, d}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	
	return
}

func guessDMY(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	re := regexp.MustCompile("([[:digit:]]+)/((?:[[:digit:]]|[[:alpha:]])+)/([[:digit:]]+)")
	if !re.MatchString(word) { 
		return 
	}

	match := re.FindStringSubmatch(word)
	y, _  := strconv.Atoi(match[3])
	m  := int(monthParseString(match[2]))
	d, _  := strconv.Atoi(match[1])

	nextGuesses = []DateGuess {}

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{y, m, d}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	
	return
}

func guessMDY(guesses []DateGuess, word string) (nextGuesses []DateGuess) {
	re := regexp.MustCompile("([[:digit:]]+)/((?:[[:digit:]]|[[:alpha:]])+)/([[:digit:]]+)")
	if !re.MatchString(word) { 
		return 
	}

	match := re.FindStringSubmatch(word)
	y, _  := strconv.Atoi(match[3])
	m  := int(monthParseString(match[1]))
	d, _  := strconv.Atoi(match[2])

	nextGuesses = []DateGuess {}

	for _, guess := range(guesses) {
		if !guess.date.isEmpty() { continue }
		copyGuess := guess
		copyGuess.date = Date{y, m, d}
		nextGuesses = append(nextGuesses, copyGuess)
	}
	
	return
}

/////

func parseDate(input string) (Date, error) {
	words := strings.Fields(input)
	guesses := []DateGuess{DateGuess{}}

	for _, word := range(words) {
		word = strings.TrimFunc(word, func(r rune) bool { return !unicode.IsDigit(r) && !unicode.IsLetter(r) })

		nextGuesses := []DateGuess{}
		nextGuesses = append(nextGuesses, guessIncrementSuffix(guesses, word)...)
		nextGuesses = append(nextGuesses, guessDecrementSuffix(guesses, word)...)
		nextGuesses = append(nextGuesses, guessIncrementType(guesses, word)...)
		nextGuesses = append(nextGuesses, guessBareNumber(guesses, word)...)
		nextGuesses = append(nextGuesses, guessBareMonth(guesses, word)...)
		nextGuesses = append(nextGuesses, guessLastNextImplyToday(guesses, word)...)
		nextGuesses = append(nextGuesses, guessTomorrow(guesses, word)...)
		nextGuesses = append(nextGuesses, guessYesterday(guesses, word)...)
		nextGuesses = append(nextGuesses, guessToday(guesses, word)...)
		nextGuesses = append(nextGuesses, guessYMD(guesses, word)...)
		nextGuesses = append(nextGuesses, guessMDY(guesses, word)...)
		nextGuesses = append(nextGuesses, guessDMY(guesses, word)...)
		guesses = nextGuesses
	}

	dates := []Date{}
	for _, guess := range(guesses) {
		if d, err := guess.flatten(); err == nil {
			dates = append(dates, d)
		} 
	}

	if len(dates) == 0 {
		return Date{}, errors.New("no dates found")
	}
	if len(dates) > 1 {
		return Date{}, errors.New("ambiguous interpretation" + fmt.Sprint(dates))
	}

	return dates[0], nil
}

func main() {
	file, err := os.Open(os.Args[1])
	if err != nil { panic(err) }
	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	
	for scanner.Scan() {
		text := strings.Trim(scanner.Text(), "\n \t")
		d, err := parseDate(text)
		if err == nil {
			fmt.Printf("%s -> %d-%.2d-%.2d\n", text, d[0], d[1], d[2])
		} else {
			fmt.Printf("%s -> error: %s\n", text, err.Error())
		}
	}
}
