// UT| g++ -o test.out {src_file}
// UT| ./test.out


struct Calculate {

// UT[ ../sample.cpp * calculate_calculate
    Calculate(int val) : value(val) { }
// UT]

    int value;
};


#include <stdio.h>

int main() {
    Calculate calculate(10);
    printf("calculate.value = %d\n", calculate.value);
    return 0;
}


// UT> calculate.value = 10
