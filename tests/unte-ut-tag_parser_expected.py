# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_expected
def tag_parser_expected(tags, value, line_no, path_dir):
    tags['expected'].append(value + '\n')
# UT]


if __name__ == "__main__":
    tags = {'expected': []}
    r = tag_parser_expected(tags, ' text ', 1, 'path_dir')
    print('result:', r, tags)


# UT> result: None {'expected': [' text \\n']}
