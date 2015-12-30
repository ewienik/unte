# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_insert_end
def tag_parser_insert_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    tag = tags['current']['insert']
    if not tag:
        return "End tag without starting tag"
    tag['end'] = line_no
    tags['current']['insert'] = None
# UT]


if __name__ == "__main__":
    tags = {}
    r = tag_parser_insert_end(tags, ' v ', 1, 'path_dir')
    print('result:', r, tags)
    tags['current'] = {'insert': None}
    r = tag_parser_insert_end(tags, ' ', 5, 'path_dir')
    print('result:', r, tags)
    last = {'end': None}
    tags['current']['insert'] = last
    r = tag_parser_insert_end(tags, ' ', 6, 'path_dir')
    print('result:', r, tags, last)


# UT> result: Wrong args for tag. There should be no args. {}
# UT> result: End tag without starting tag {'current': {'insert': None}}
# UT> result: None {'current': {'insert': None}} {'end': 6}
