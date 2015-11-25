# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * find_files
def find_files(globs):
    assert '__iter__' in dir(globs)
    print('find_files(...)')

    result = []

    for pathname in globs:
        path_dir, sep, path_file = pathname.partition('**')
        if len(sep) == 0:
            find_files_glob(result, pathname)
            continue

        if len(path_dir) == 0 or os.path.isdir(path_dir):
            find_files_walk(result, path_dir, path_file)

    return result
# UT]


class os:  # noqa

    class path:  # noqa

        # UT( externals.py * os_path_isdir
        @staticmethod
        def isdir(path):
            assert type(path) == str
            print('os.path.isdir(%s)' % path)
        # UT)
            r = ('not_dir' not in path)
            print('return %s' % r)
            return r


# UT( ../unte.py * find_files_glob
def find_files_glob(result, pathname):
    assert type(result) == list
    assert type(pathname) == str
    print('find_files_glob(%s, %s)' % (result, pathname))
# UT)
    add = 'glob.%s' % pathname
    result.append(add)
    print('add result %s' % add)


# UT( ../unte.py * find_files_walk
def find_files_walk(result, path_dir, path_file):
    assert type(result) == list
    assert type(path_dir) == str
    assert type(path_file) == str
    print('find_files_walk(%s, %s, %s)' % (result, path_dir, path_file))
# UT)
    add = 'walk.%s.%s' % (path_dir, path_file)
    result.append(add)
    print('add result %s' % add)


if __name__ == "__main__":
    paths = [
        'd1/d2/*.e1', '**/*.e2', '/**/*.e3', 'not_dir/**/*.e4', 'd3/**/*.e5'
    ]
    print('paths:', paths)
    print('result:', find_files(paths))


# noqa UT> paths: ['d1/d2/*.e1', '**/*.e2', '/**/*.e3', 'not_dir/**/*.e4', 'd3/**/*.e5']
# UT> find_files(...)
# UT> find_files_glob([], d1/d2/*.e1)
# UT> add result glob.d1/d2/*.e1
# UT> find_files_walk(['glob.d1/d2/*.e1'], , /*.e2)
# UT> add result walk../*.e2
# UT> os.path.isdir(/)
# UT> return True
# UT> find_files_walk(['glob.d1/d2/*.e1', 'walk../*.e2'], /, /*.e3)
# UT> add result walk././*.e3
# UT> os.path.isdir(not_dir/)
# UT> return False
# UT> os.path.isdir(d3/)
# UT> return True
# noqa UT> find_files_walk(['glob.d1/d2/*.e1', 'walk../*.e2', 'walk././*.e3'], d3/, /*.e5)
# UT> add result walk.d3/./*.e5
# noqa UT> result: ['glob.d1/d2/*.e1', 'walk../*.e2', 'walk././*.e3', 'walk.d3/./*.e5']
