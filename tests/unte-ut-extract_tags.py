# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * extract_tags
def extract_tags(path):
    tags = {
        'current': {
            'definition': [],
            'insert': None,
        },
        'definition': {},
        'insert': [],
        'assert': [],
        'exec': [],
        'expected': [],
    }

    ok = True
    f = open(path)
    line_no = 0
    path_dir = os.path.dirname(path)
    for line in f:
        line_no += 1

        tag_type, tag_value = tag_get(line)
        if tag_type is None or tag_value is None:
            continue
        err = tag_parse(tags, tag_type, tag_value, line_no, path_dir)
        if err:
            print('\n%s:%d:error:%s' % (path, line_no, err), end='')
            ok = False

    if not ok:
        print('')
        sys.exit(1)

    return tags
# UT]


from pprint import pformat


def open(path):
    r = [
        'line1',
        '.v',
        't.',
        't.v',
    ]
    print('open(%s): %s' % (path, r))
    return r


class os:  # noqa
    class path:  # noqa
        @staticmethod
        def dirname(path):
            r = 'dirname.' + path
            print('os.path.dirname(%s): %s' % (path, r))
            return r


class sys:  # noqa
    @staticmethod
    def exit(value):
        print('sys.exit(%d)' % value)


def tag_get(line):
    tab = line.split('.')
    t, v = None, None
    if len(tab) > 0 and len(tab[0]) > 0:
        t = tab[0]
    if len(tab) > 1 and len(tab[1]) > 0:
        v = tab[1]
    print('tag_get(%s): %s, %s' % (line, t, v))
    return t, v


def tag_parse(tags, tag_type, tag_value, line_no, path_dir):
    print('tag_parse(%s, %s, %s, %d, %s): %s' % (
        pformat(tags), tag_type, tag_value, line_no, path_dir,
        tag_parse.result
    ))
    return tag_parse.result
tag_parse.result = None


if __name__ == "__main__":
    r = extract_tags('path1')
    print('result:', pformat(r))
    tag_parse.result = "Error parsing"
    extract_tags('path2')


# UT> open(path1): ['line1', '.v', 't.', 't.v']
# UT> os.path.dirname(path1): dirname.path1
# UT> tag_get(line1): line1, None
# UT> tag_get(.v): None, v
# UT> tag_get(t.): t, None
# UT> tag_get(t.v): t, v
# UT> tag_parse({'assert': [],
# UT>  'current': {'definition': [], 'insert': None},
# UT>  'definition': {},
# UT>  'exec': [],
# UT>  'expected': [],
# UT>  'insert': []}, t, v, 4, dirname.path1): None
# UT> result: {'assert': [],
# UT>  'current': {'definition': [], 'insert': None},
# UT>  'definition': {},
# UT>  'exec': [],
# UT>  'expected': [],
# UT>  'insert': []}
# UT> open(path2): ['line1', '.v', 't.', 't.v']
# UT> os.path.dirname(path2): dirname.path2
# UT> tag_get(line1): line1, None
# UT> tag_get(.v): None, v
# UT> tag_get(t.): t, None
# UT> tag_get(t.v): t, v
# UT> tag_parse({'assert': [],
# UT>  'current': {'definition': [], 'insert': None},
# UT>  'definition': {},
# UT>  'exec': [],
# UT>  'expected': [],
# UT>  'insert': []}, t, v, 4, dirname.path2): Error parsing
# UT>
# UT> path2:4:error:Error parsing
# UT> sys.exit(1)
