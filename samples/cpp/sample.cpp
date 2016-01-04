#include <stdlib.h>
#include <stdio.h>


struct Calculate {

    // UT{ calculate_calculate
    Calculate(int val) : value(val) { }
    // UT}

    // UT{ calculate_calc
    int calc(int val) {
        return value * val;
    }
    // UT}

private:
    int value;
};

// UT{ entry_point
int entry_point(int argc, char const ** argv) {
    if (2 != argc) {
        printf("Wrong arguments. Should be one number\n");
        return 1;
    }
    Calculate calculate(4);
    int value = atoi(argv[1]);
    printf("Input value = %d\n", value);
    printf("Result = %d\n", calculate.calc(value));
    return 0;
}
// UT}


int main(int argc, char const ** argv) {
    return entry_point(argc, argv);
}
