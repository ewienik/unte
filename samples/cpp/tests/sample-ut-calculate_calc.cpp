// UT| g++ -o test.out {src_file}
// UT| ./test.out


struct Calculate {

// UT[ ../sample.cpp * calculate_calc
    int calc(int val) {
        return value * val;
    }
// UT]

    int value;
};


#include <stdio.h>

int main() {
    Calculate calculate;
    calculate.value = 20;
    printf("calc = %d\n", calculate.calc(3));
    return 0;
}


// UT> calc = 60
