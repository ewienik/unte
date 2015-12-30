# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * diff_file
def diff_file(path, tags, output):
    ok = True
    diff = []
    for line in difflib.context_diff(
        tags['expected'], output, fromfile='EXPECTED', tofile='OUTPUT',
    ):
        ok = False
        diff.append(line)

    if not ok:
        print('\n%s:1:error:There is unexpected output' % path)
        for line in diff:
            sys.stdout.write(line)
        return False

    return True
# UT]


class difflib:  # noqa
    diff_result = []

    @staticmethod
    def context_diff(expected, output, fromfile='', tofile=''):
        print('difflib.context_diff(%s, %s, fromfile=%s, tofile=%s): %s' % (
            expected, output, fromfile, tofile, difflib.diff_result
        ))
        return difflib.diff_result


class sys:  # noqa
    class stdout:  # noqa
        @staticmethod
        def write(line):
            print('sys.stdout.write(%s)' % line)


if __name__ == "__main__":
    r = diff_file('path', {'expected': 'expected'}, 'output')
    print('result = %s' % r)
    difflib.diff_result = ['diff1', 'diff2']
    r = diff_file('path', {'expected': 'expected'}, 'output')
    print('result = %s' % r)


# noqa UT> difflib.context_diff(expected, output, fromfile=EXPECTED, tofile=OUTPUT): []
# UT> result = True
# noqa UT> difflib.context_diff(expected, output, fromfile=EXPECTED, tofile=OUTPUT): ['diff1', 'diff2']
# UT>
# UT> path:1:error:There is unexpected output
# UT> sys.stdout.write(diff1)
# UT> sys.stdout.write(diff2)
# UT> result = False
