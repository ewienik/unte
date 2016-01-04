// UT| go run {src_file}

package main

import (
	"fmt"
)

// UT[ ../sample.go * calculate
func calculate(value int) int {
	return value * value
}

// UT]

func main() {
	fmt.Printf("calculate = %d\n", calculate(4))
}

// UT> calculate = 16
