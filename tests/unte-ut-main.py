# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * main
def main():
    args = parse_args()
    paths = find_files(args.paths)

    counters = {
        'for_processing': len(paths),
        'processed': 0,
        'passed': 0,
        'failed': 0,
    }

    result = 0
    for path in paths:
        if not process_file(path, counters):
            result = 1

    print_summary(counters)
    sys.exit(result)
# UT]


class sys:  # noqa
    @staticmethod
    def exit(value):
        print('sys.exit(%d)' % value)


def find_files(paths):
    r = [elem for path in paths for elem in path.split('.')]
    print('find_files(%s): %s' % (paths, r))
    return r


def parse_args():
    r = type('dummy', (), {'paths': parse_args.result})
    print('parse_args(): %s' % r.paths)
    return r
parse_args.result = ['p1.p2', 'p3.p4']


def print_summary(counters):
    print('print_summary(%s)' % counters)


def process_file(path, counters):
    r = ('0' not in path)
    print('process_file(%s, %s): %s' % (path, counters, r))
    return r


if __name__ == "__main__":
    main()
    parse_args.result = ['p7.p0', 'p5.p6']
    main()


# UT> parse_args(): ['p1.p2', 'p3.p4']
# UT> find_files(['p1.p2', 'p3.p4']): ['p1', 'p2', 'p3', 'p4']
# noqa UT> process_file(p1, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> process_file(p2, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> process_file(p3, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> process_file(p4, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> print_summary({'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4})
# UT> sys.exit(0)
# UT> parse_args(): ['p7.p0', 'p5.p6']
# UT> find_files(['p7.p0', 'p5.p6']): ['p7', 'p0', 'p5', 'p6']
# noqa UT> process_file(p7, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> process_file(p0, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): False
# noqa UT> process_file(p5, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> process_file(p6, {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4}): True
# noqa UT> print_summary({'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 4})
# UT> sys.exit(1)
