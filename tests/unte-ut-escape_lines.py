# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * escape_lines
def escape_lines(lines):
    i = 0
    while i < len(lines):
        line = lines[i]
        if len(line) == 0:
            i += 1
            continue
        if line[-1] == '\n':
            line = line[:-1]
        line = repr(line)[1:-1] + '\n'
        lines[i] = line
        i += 1
# UT]


if __name__ == "__main__":
    lines = ['', '\n', '\r', 'line\t1', 'line\t2']
    print("lines:", lines)
    escape_lines(lines)
    print("lines:", lines)


# UT> lines: ['', '\\n', '\\r', 'line\\t1', 'line\\t2']
# UT> lines: ['', '\\n', '\\\\r\\n', 'line\\\\t1\\n', 'line\\\\t2\\n']
