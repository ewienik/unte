# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_exec_check
def tag_parser_exec_check(tags, value, line_no, path_dir):
    cmd = value.strip()
    if len(cmd) == 0:
        return "Should be a command."
    tags['exec'].append({'check': True, 'cmd': cmd})
# UT]


if __name__ == "__main__":
    tags = {}
    r = tag_parser_exec_check(tags, ' ', 1, 'path_dir')
    print('result:', r, tags)
    tags['exec'] = []
    r = tag_parser_exec_check(tags, ' cmd ', 5, 'path_dir')
    print('result:', r, tags)


# UT> result: Should be a command. {}
# UT> result: None {'exec': [{'cmd': 'cmd', 'check': True}]}
