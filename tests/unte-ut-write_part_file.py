# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * write_part_file
def write_part_file(dst, tags, tag_path, tag_name):
    if tag_path not in tags:
        return
    definition = tags[tag_path]['definition']
    tag_child = definition.get(tag_name)
    if tag_child:
        write_part_file_one(
            dst, tag_path,
            tag_child['start'], tag_child['end']
        )
# UT]


def write_part_file_one(dst, src, start, end):
    print('write_part_file_one(%s, %s, %s, %s)' % (dst, src, start, end))


if __name__ == "__main__":
    tags = {}
    write_part_file('dst', tags, 'path', 'name1')
    tags = {'path': {'definition': {}}}
    write_part_file('dst', tags, 'path', 'name2')
    tags['path']['definition']['name3'] = {'start': 'start', 'end': 'end'}
    write_part_file('dst', tags, 'path', 'name3')


# UT> write_part_file_one(dst, path, start, end)
