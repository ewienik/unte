# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * update_file
def update_file(path, tags):
    tags_db = dict([
        [tag['file'], extract_tags(tag['file'])]
        for tag in tags['insert']
    ])

    temp_dst = tempfile.TemporaryFile(mode='w+')
    compile_file(temp_dst, path, tags, tags_db)
    temp_dst.seek(0)
    shutil.copyfileobj(temp_dst, open(path, 'w'))
# UT]


class tempfile:  # noqa
    class TemporaryFile:
        id = 0

        def __init__(self, mode=''):
            self.id = tempfile.TemporaryFile.id
            tempfile.TemporaryFile.id += 1
            print('tempfile.TemporaryFile.__init__(%d, mode=%s)' % (
                self.id, mode
            ))

        def seek(self, value):
            print('tempfile.TemporaryFile.seek(%d, %s)' % (self.id, value))


class shutil:  # noqa
    @staticmethod
    def copyfileobj(src, dst):
        print('shutil.copyfileobj(%s, %s)' % (src.id, dst))


def compile_file(dst, src, tags, tags_db):
    print('compile_file(\n    %s,\n    %s,\n    %s,\n    %s\n)' % (
        dst.id, src, tags, tags_db
    ))


def extract_tags(path):
    r = 'tags_from.' + path
    print('extract_tags(%s): %s' % (path, r))
    return r


def open(path, mode):
    r = 'open.' + path
    print('open(%s, %s): %s' % (path, mode, r))
    return r

if __name__ == "__main__":
    update_file('path', {'insert': [{'file': 'f1'}, {'file': 'f2'}]})


# UT> extract_tags(f1): tags_from.f1
# UT> extract_tags(f2): tags_from.f2
# UT> tempfile.TemporaryFile.__init__(0, mode=w+)
# UT> compile_file(
# UT>     0,
# UT>     path,
# UT>     {'insert': [{'file': 'f1'}, {'file': 'f2'}]},
# UT>     {'f1': 'tags_from.f1', 'f2': 'tags_from.f2'}
# UT> )
# UT> tempfile.TemporaryFile.seek(0, 0)
# UT> open(path, w): open.path
# UT> shutil.copyfileobj(0, open.path)
