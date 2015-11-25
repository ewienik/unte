# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * find_files_walk
def find_files_walk(result, path_dir, path_file):
    assert type(result) == list
    assert type(path_dir) == str
    assert type(path_file) == str
    print('find_files_walk(%s, %s, %s)' % (result, path_dir, path_file))

    pattern = os.path.basename(path_file)
    for root, dirs, files in os.walk(path_dir):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                result.append(os.path.join(root, f))
# UT]


class fnmatch:  # noqa
    # UT( externals.py * fnmatch_fnmatch
    @staticmethod
    def fnmatch(f, pattern):
        assert type(f) == str
        assert type(pattern) == str
        print('fnmatch.fnmatch(%s, %s)' % (f, pattern))
    # UT)
        r = (f == pattern)
        print('return %s' % r)
        return r


class glob:  # noqa
    # UT( externals.py * glob_glob
    @staticmethod
    def glob(path):
        assert type(path) == str
        print('glob.glob(%s)' % path)
    # UT)
        yield 'not-exist'
        yield 'exist'


class os:  # noqa

    # UT( externals.py * os_walk
    @staticmethod
    def walk(path):
        assert type(path) == str
        print('os.walk(%s)' % path)
    # UT)
        yield 'root', ['dir1', 'dir2'], ['file1', 'file2', 'basename.pathname']

    class path:  # noqa

        # UT( externals.py * os_path_basename
        @staticmethod
        def basename(path):
            assert type(path) == str
            print('os.path.basename(%s)' % path)
        # UT)
            r = 'basename.%s' % path
            print('return %s' % r)
            return r

        # UT( externals.py * os_path_join
        @staticmethod
        def join(*args):
            for arg in args:
                assert type(arg) == str
            print('os.path.join(%s)' % str(args))
        # UT)
            r = '.'.join(args)
            print('return %s' % r)
            return r


if __name__ == "__main__":
    result = []
    find_files_walk(result, 'pathdir', 'pathname')
    print('result:', result)


# UT> find_files_walk([], pathdir, pathname)
# UT> os.path.basename(pathname)
# UT> return basename.pathname
# UT> os.walk(pathdir)
# UT> fnmatch.fnmatch(file1, basename.pathname)
# UT> return False
# UT> fnmatch.fnmatch(file2, basename.pathname)
# UT> return False
# UT> fnmatch.fnmatch(basename.pathname, basename.pathname)
# UT> return True
# UT> os.path.join(('root', 'basename.pathname'))
# UT> return root.basename.pathname
# UT> result: ['root.basename.pathname']
