// UT| gcc -o test.out {src_file}
// UT| ./test.out

#include <stdio.h>

int atoi(char const * txt) {
    int r = txt[0] - '0';
    printf("atoi(%s): %d\n", txt, r);
    return r;
}


int calculate(int value) {
    int r = value + 1;
    printf("calculate(%d): %d\n", value, r);
    return r;
}

// UT[ ../sample.c * entry_point
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
// UT]


int main() {
    char * args[] = { "test.out", NULL, NULL };
    printf("result = %d\n", entry_point(1, args));
    args[1] = "23";
    printf("result = %d\n", entry_point(2, args));
    return 0;
}


// UT> Wrong arguments. Should be one number
// UT> result = 1
// UT> atoi(23): 2
// UT> Input value = 2
// UT> calculate(2): 3
// UT> Result = 3
// UT> result = 0
