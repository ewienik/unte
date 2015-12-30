# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * tag_parser_insert_start
def tag_parser_insert_start(tags, value, line_no, path_dir):
    outer = tags['current']['insert']
    if outer:
        return "Tag inside other (outer defined in line %d)." % outer['start']

    args = value.split('*')
    if len(args) != 2:
        return "There should be two args: a path and a tag name."
    path = args[0].strip()
    if len(path) == 0:
        return "Path arg is empty."
    name = args[1].strip()
    if len(name) == 0:
        return "Tag name arg is empty."

    tag = {
        'name': name,
        'file': os.path.join(path_dir, path),
        'start': line_no,
        'end': None,
    }
    tags['insert'].append(tag)
    tags['current']['insert'] = tag
# UT]


class os:  # noqa
    class path:  # noqa
        @staticmethod
        def join(*args):
            r = '.'.join(args)
            print('os.path.join(%s): %s' % (str(args), r))
            return r

if __name__ == "__main__":
    tags = {'current': {'insert': {'start': 2}}}
    r = tag_parser_insert_start(tags, ' ', 3, 'path_dir')
    print('result:', r, tags)
    tags['current']['insert'] = None
    r = tag_parser_insert_start(tags, ' p t ', 4, 'path_dir')
    print('result:', r, tags)
    r = tag_parser_insert_start(tags, '  * t ', 4, 'path_dir')
    print('result:', r, tags)
    r = tag_parser_insert_start(tags, ' p *  ', 4, 'path_dir')
    print('result:', r, tags)
    tags['insert'] = []
    r = tag_parser_insert_start(tags, ' p * t ', 5, 'path_dir')
    print('result:', r, tags)


# noqa UT> result: Tag inside other (outer defined in line 2). {'current': {'insert': {'start': 2}}}
# noqa UT> result: There should be two args: a path and a tag name. {'current': {'insert': None}}
# UT> result: Path arg is empty. {'current': {'insert': None}}
# UT> result: Tag name arg is empty. {'current': {'insert': None}}
# UT> os.path.join(('path_dir', 'p')): path_dir.p
# noqa UT> result: None {'current': {'insert': {'start': 5, 'end': None, 'name': 't', 'file': 'path_dir.p'}}, 'insert': [{'start': 5, 'end': None, 'name': 't', 'file': 'path_dir.p'}]}
