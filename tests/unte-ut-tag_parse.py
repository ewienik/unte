# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parse
def tag_parse(tags, tag_type, tag_value, line_no, path_dir):
    if tag_type not in TAG_PARSERS:
        return "Unknown tag type '%s'" % tag_type
    return TAG_PARSERS[tag_type](tags, tag_value, line_no, path_dir)
# UT]


def parser(tags, tag_value, line_no, path_dir):
    r = 'rparser'
    print('parser(%s, %s, %d, %s): %s' % (
        tags, tag_value, line_no, path_dir, r,
    ))
    return r


TAG_PARSERS = {'t': parser}


if __name__ == "__main__":
    print('result:', tag_parse({}, 't', 'v', 3, 'path'))
    print('result:', tag_parse({}, 'n', 'v', 3, 'path'))


# UT> parser({}, v, 3, path): rparser
# UT> result: rparser
# UT> result: Unknown tag type 'n'
