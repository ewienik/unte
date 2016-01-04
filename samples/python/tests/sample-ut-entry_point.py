# UT| python {src_file}


# UT[ ../sample.py * entry_point
def entry_point():
    if len(sys.argv) != 2:
        print "Wrong arguments. Should be one number"
        return 1
    value = int(sys.argv[1])
    print "Input value =", value
    print "Result =", calculate(value)
    return 0
# UT]


class sys:  # noqa
    argv = []


def calculate(value):
    r = value * 2
    print "calculate(%s): %d" % (value, r)
    return r


print "entry_point =", entry_point()
sys.argv = ["prog", "23"]
print "entry_point =", entry_point()


# UT> entry_point = Wrong arguments. Should be one number
# UT> 1
# UT> entry_point = Input value = 23
# UT> Result = calculate(23): 46
# UT> 46
# UT> 0
