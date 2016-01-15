# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * escape_lines
def escape_lines(lines):
    i = 0
    start = 2 if sys.version_info < (3, 0) else 1
    while i < len(lines):
        line = lines[i]
        if len(line) == 0:
            i += 1
            continue
        if line[-1] == '\n':
            line = line[:-1]
        line = repr(line)[start:-1] + '\n'
        lines[i] = line
        i += 1
# UT]


class sys:  # noqa
    version_info = (2, 7)


if __name__ == "__main__":
    lines = [u'', u'\n', u'\r', u'line\t1', u'line\t2']
    print("lines:", lines)
    escape_lines(lines)
    print("lines:", lines)


# UT> lines: [u'', u'\\n', u'\\r', u'line\\t1', u'line\\t2']
# UT> lines: [u'', '\\n', '\\\\r\\n', 'line\\\\t1\\n', 'line\\\\t2\\n']
