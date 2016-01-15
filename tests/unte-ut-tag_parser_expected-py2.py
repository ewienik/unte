# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_expected
def tag_parser_expected(tags, value, line_no, path_dir):
    line = value + '\n'
    if sys.version_info < (3, 0):
        line = unicode(line)
    tags['expected'].append(line)
# UT]


class sys:  # noqa
    version_info = (2, 7)


if __name__ == "__main__":
    tags = {'expected': []}
    r = tag_parser_expected(tags, ' text ', 1, 'path_dir')
    print('result:', r, tags)


# UT> result: None {'expected': [u' text \\n']}
