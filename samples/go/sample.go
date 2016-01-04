package main

import (
	"fmt"
	"os"
	"strconv"
)

// UT{ calculate
func calculate(value int) int {
	return value * value
}

// UT}

// UT{ entry_point
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

// UT}

func main() {
	os.Exit(entry_point())
}
