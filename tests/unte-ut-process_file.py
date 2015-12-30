# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * process_file
def process_file(path, counters):
    ok = True
    counters['processed'] += 1
    print('\rProcessing %d/%d file ... ' % (
        counters['processed'], counters['for_processing']
    ), end='')
    sys.stdout.flush()
    try:
        tags = extract_tags(path)
        update_file(path, tags)
        status, output = execute_file(path, tags)
        if not status:
            ok = False
        else:
            escape_lines(output)
            if not diff_file(path, tags, output):
                ok = False
    except:
        ok = False
        traceback.print_exc()
    if ok:
        counters['passed'] += 1
    else:
        counters['failed'] += 1
        print('Error in', path)

    return ok
# UT]


class sys:  # noqa
    class stdout:  # noqa
        @staticmethod
        def flush():
            print('sys.stdout.flush()')


class traceback:  # noqa
    @staticmethod
    def print_exc():
        print('traceback.print_exc()')


def diff_file(path, tags, output):
    print('diff_file(%s, %s, %s): %s' % (
        path, tags, output, diff_file.result
    ))
    return diff_file.result
diff_file.result = False


def escape_lines(lines):
    print('escape_lines(%s)' % lines)


def execute_file(path, tags):
    r = 'output'
    print('execute_file(%s, %s): %s, %s' % (
        path, tags, execute_file.status, r
    ))
    return execute_file.status, r
execute_file.status = False


def extract_tags(path):
    if extract_tags.exception:
        r = 'Exception'
    else:
        r = 'tags'
    print('extract_tags(%s): %s' % (path, r))
    if extract_tags.exception:
        raise Exception('test exception')
    return r
extract_tags.exception = True


def update_file(path, tags):
    print('update_file(%s)' % path)


if __name__ == "__main__":
    counters = {
        'for_processing': 10,
        'processed': 0,
        'passed': 0,
        'failed': 0,
    }
    print('counters:', counters)

    process_file('path1', counters)
    print('counters:', counters)

    extract_tags.exception = False
    process_file('path2', counters)
    print('counters:', counters)

    execute_file.status = True
    process_file('path3', counters)
    print('counters:', counters)

    diff_file.result = True
    process_file('path4', counters)
    print('counters:', counters)


# noqa UT> counters: {'failed': 0, 'processed': 0, 'passed': 0, 'for_processing': 10}
# UT> \r
# UT> Processing 1/10 file ... sys.stdout.flush()
# UT> extract_tags(path1): Exception
# UT> traceback.print_exc()
# UT> Error in path1
# noqa UT> counters: {'failed': 1, 'processed': 1, 'passed': 0, 'for_processing': 10}
# UT> \r
# UT> Processing 2/10 file ... sys.stdout.flush()
# UT> extract_tags(path2): tags
# UT> update_file(path2)
# UT> execute_file(path2, tags): False, output
# UT> Error in path2
# noqa UT> counters: {'failed': 2, 'processed': 2, 'passed': 0, 'for_processing': 10}
# UT> \r
# UT> Processing 3/10 file ... sys.stdout.flush()
# UT> extract_tags(path3): tags
# UT> update_file(path3)
# UT> execute_file(path3, tags): True, output
# UT> escape_lines(output)
# UT> diff_file(path3, tags, output): False
# UT> Error in path3
# noqa UT> counters: {'failed': 3, 'processed': 3, 'passed': 0, 'for_processing': 10}
# UT> \r
# UT> Processing 4/10 file ... sys.stdout.flush()
# UT> extract_tags(path4): tags
# UT> update_file(path4)
# UT> execute_file(path4, tags): True, output
# UT> escape_lines(output)
# UT> diff_file(path4, tags, output): True
# noqa UT> counters: {'failed': 3, 'processed': 4, 'passed': 1, 'for_processing': 10}
