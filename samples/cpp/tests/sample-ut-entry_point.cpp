// UT| g++ -o test.out {src_file}
// UT| ./test.out

#include <stdio.h>

int atoi(char const * txt) {
    int r = txt[0] - '0';
    printf("atoi(%s): %d\n", txt, r);
    return r;
}


struct Calculate {
    Calculate(int val) {
        id = id_counter++;
        printf("Calculate::Calculate(%d, %d)\n", id, val);
    }

    int calc(int val) {
        int r = val * 5;
        printf("Calculate::calc(%d, %d): %d\n", id, val, r);
        return r;
    }

    static int id_counter;
    int id;
};

int Calculate::id_counter = 0;

// UT[ ../sample.cpp * entry_point
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
// UT]


int main() {
    char const * args[] = { "test.out", NULL, NULL };
    printf("result = %d\n", entry_point(1, args));
    args[1] = "23";
    printf("result = %d\n", entry_point(2, args));
    return 0;
}


// UT> Wrong arguments. Should be one number
// UT> result = 1
// UT> Calculate::Calculate(0, 4)
// UT> atoi(23): 2
// UT> Input value = 2
// UT> Calculate::calc(0, 2): 10
// UT> Result = 10
// UT> result = 0
