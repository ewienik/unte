// UT| go run {src_file}

package main

import (
	"fmt"
)

// UT[ ../sample.go * entry_point
func entry_point() int {
	if len(os.Args) != 2 {
		fmt.Println("Wrong arguments. Should be one number")
		return 1
	}
	value, _ := strconv.Atoi(os.Args[1])
	fmt.Printf("Input value = %d\n", value)
	fmt.Printf("Result = %d\n", calculate(value))
	return 0
}

// UT]

func calculate(value int) int {
	r := value * 3
	fmt.Printf("calculate(%d): %d\n", value, r)
	return r
}

type os_t struct {
	Args []string
}

var os os_t

type strconv_t struct {
}

var strconv strconv_t

func (sc strconv_t) Atoi(txt string) (int, error) {
	r := 10
	fmt.Printf("strconv.Atoi(%s): %d\n", txt, r)
	return r, nil
}

func main() {
	fmt.Printf("result = %d\n", entry_point())
	os.Args = []string{"prog", "23"}
	fmt.Printf("result = %d\n", entry_point())
}

// UT> Wrong arguments. Should be one number
// UT> result = 1
// UT> strconv.Atoi(23): 10
// UT> Input value = 10
// UT> calculate(10): 30
// UT> Result = 30
// UT> result = 0
