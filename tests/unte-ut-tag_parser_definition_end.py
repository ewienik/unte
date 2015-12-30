# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_definition_end
def tag_parser_definition_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    stack = tags['current']['definition']
    if len(stack) == 0:
        return "End tag without starting tag"
    stack.pop()['end'] = line_no
# UT]


if __name__ == "__main__":
    tags = {}
    r = tag_parser_definition_end(tags, ' v ', 1, 'path_dir')
    print('result:', r, tags)
    tags['current'] = {'definition': []}
    r = tag_parser_definition_end(tags, ' ', 5, 'path_dir')
    print('result:', r, tags)
    last = {}
    tags['current']['definition'].append(last)
    r = tag_parser_definition_end(tags, ' ', 6, 'path_dir')
    print('result:', r, tags, last)


# UT> result: Wrong args for tag. There should be no args. {}
# UT> result: End tag without starting tag {'current': {'definition': []}}
# UT> result: None {'current': {'definition': []}} {'end': 6}
