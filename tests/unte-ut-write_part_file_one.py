# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * write_part_file_one
def write_part_file_one(dst, src, start, end):
    f = open(src)
    line_no = 0
    state = 'normal'
    for line in f:
        line_no += 1
        if state == 'inside':
            if end == line_no:
                return
            dst.write(line)
            continue
        if start == line_no:
            state = 'inside'
# UT]


def open(path):
    r = [
        'l1',
        'l2',
        'l3',
        'l4',
        'l5',
    ]
    print('open(%s): %s' % (path, r))
    return r


def write(self, line):
    print('write(%s)' % line)


if __name__ == "__main__":
    write_part_file_one(type('dummy', (), {'write': write})(), 'src', 2, 4)


# UT> open(src): ['l1', 'l2', 'l3', 'l4', 'l5']
# UT> write(l3)
