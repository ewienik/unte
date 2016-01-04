#include <stdlib.h>
#include <stdio.h>


// UT{ calculate
int calculate(int value) {
    return value * value;
}
// UT}


// UT{ entry_point
int entry_point(int argc, char ** argv) {
    if (2 != argc) {
        printf("Wrong arguments. Should be one number\n");
        return 1;
    }
    int value = atoi(argv[1]);
    printf("Input value = %d\n", value);
    printf("Result = %d\n", calculate(value));
    return 0;
}
// UT}


int main(int argc, char ** argv) {
    return entry_point(argc, argv);
}
