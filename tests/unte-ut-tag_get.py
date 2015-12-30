# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_get
def tag_get(line):
    match = PROG_TAG.match(line)
    if match is not None:
        return match.group(1), match.group(2)
    return None, None
# UT]


import re

PROG_TAG = re.compile('match1-(group1)-match2-(group2)')


if __name__ == "__main__":
    print('result:', tag_get("line1"))
    print('result:', tag_get("match1-group1-match2-group2"))


# UT> result: (None, None)
# UT> result: ('group1', 'group2')
