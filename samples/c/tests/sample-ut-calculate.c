// UT| gcc -o test.out {src_file}
// UT| ./test.out


// UT[ ../sample.c * calculate
int calculate(int value) {
    return value * value;
}
// UT]


#include <stdio.h>

int main() {
    printf("calculate = %d\n", calculate(3));
    return 0;
}


// UT> calculate = 9
