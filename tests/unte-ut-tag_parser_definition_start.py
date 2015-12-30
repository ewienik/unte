# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_definition_start
def tag_parser_definition_start(tags, value, line_no, path_dir):
    name = value.strip()
    if len(name) == 0:
        return "There is no a tag name."
    if name in tags['definition']:
        return "Duplicate start of tag '%s' (previous at %d)" % (
            name, tags['definition'][name]['start']
        )
    tag = {'start': line_no, 'end': None}
    tags['definition'][name] = tag
    tags['current']['definition'].append(tag)
# UT]


if __name__ == "__main__":
    tags = {}
    r = tag_parser_definition_start(tags, ' ', 1, 'path_dir')
    print('result:', r, tags)
    tags['definition'] = {'v1': {'start': 2}}
    r = tag_parser_definition_start(tags, ' v1 ', 5, 'path_dir')
    print('result:', r, tags)
    tags['definition'] = {}
    tags['current'] = {'definition': []}
    r = tag_parser_definition_start(tags, ' v2 ', 6, 'path_dir')
    print('result:', r, tags)


# UT> result: There is no a tag name. {}
# noqa UT> result: Duplicate start of tag 'v1' (previous at 2) {'definition': {'v1': {'start': 2}}}
# noqa UT> result: None {'current': {'definition': [{'start': 6, 'end': None}]}, 'definition': {'v2': {'start': 6, 'end': None}}}
