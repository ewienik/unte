#!/usr/bin/env python2

import sys


# UT{ calculate
def calculate(value):
    return value * value
# UT}


# UT{ entry_point
def entry_point():
    if len(sys.argv) != 2:
        print "Wrong arguments. Should be one number"
        return 1
    value = int(sys.argv[1])
    print "Input value =", value
    print "Result =", calculate(value)
    return 0
# UT}


if __name__ == "__main__":
    sys.exit(entry_point())
