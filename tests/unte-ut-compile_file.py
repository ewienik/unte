# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * compile_file
def compile_file(dst, src, tags_master, tags_db):
    f = open(src)
    tag_iter = iter(enumerate_tags(tags_master))
    try:
        tag = next(tag_iter)
    except StopIteration:
        tag = None
    line_no = 0
    inside_tag = False
    for line in f:
        line_no += 1
        if inside_tag and tag['end'] == line_no:
            inside_tag = False
            try:
                tag = next(tag_iter)
            except StopIteration:
                tag = None
        if inside_tag:
            continue
        dst.write(line)
        if tag is not None and tag['start'] == line_no:
            inside_tag = True
            write_part_file(dst, tags_db, tag['file'], tag['name'])
# UT]


def enumerate_tags(tags):
    print('enumerate_tags(%s)' % tags)
    for i in range(int(tags.split('.')[1])):
        yield {
            'start': i*2 + 1,
            'end': i*2 + 2,
            'file': 'file%d' % i,
            'name': 'name%d' % i,
        }


def open(path):
    r = [
        'l1',
        'l2',
        'l3',
        'l4',
        'l5',
        'l6',
    ]
    print('open(%s): %s' % (path, r))
    return r


def write(self, line):
    print('write(%s)' % line)


def write_part_file(dst, tags, path, name):
    print('write_part_file(%s, %s, %s, %s)' % (dst.id, tags, path, name))


if __name__ == "__main__":
    dst = type('dummy', (), {'id': 0, 'write': write})()
    compile_file(dst, 'src', 'tags_master.0', 'tags_db')
    compile_file(dst, 'src', 'tags_master.2', 'tags_db')


# UT> open(src): ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']
# UT> enumerate_tags(tags_master.0)
# UT> write(l1)
# UT> write(l2)
# UT> write(l3)
# UT> write(l4)
# UT> write(l5)
# UT> write(l6)
# UT> open(src): ['l1', 'l2', 'l3', 'l4', 'l5', 'l6']
# UT> enumerate_tags(tags_master.2)
# UT> write(l1)
# UT> write_part_file(0, tags_db, file0, name0)
# UT> write(l2)
# UT> write(l3)
# UT> write_part_file(0, tags_db, file1, name1)
# UT> write(l4)
# UT> write(l5)
# UT> write(l6)
