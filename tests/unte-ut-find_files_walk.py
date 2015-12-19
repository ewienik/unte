# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * find_files_walk
def find_files_walk(result, path_dir, path_file):
    pattern = os.path.basename(path_file)
    for root, dirs, files in os.walk(path_dir):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                result.append(os.path.join(root, f))
# UT]


class fnmatch:  # noqa
    @staticmethod
    def fnmatch(f, pattern):
        r = (f == pattern)
        print('fnmatch.fnmatch(%s, %s): %s' % (f, pattern, r))
        return r


class glob:  # noqa
    @staticmethod
    def glob(path):
        print('glob.glob(%s)' % path)
        yield 'not-exist'
        yield 'exist'


class os:  # noqa

    @staticmethod
    def walk(path):
        print('os.walk(%s)' % path)
        yield 'root', ['dir1', 'dir2'], ['file1', 'file2', 'basename.pathname']

    class path:  # noqa

        @staticmethod
        def basename(path):
            r = 'basename.%s' % path
            print('os.path.basename(%s): %s' % (path, r))
            return r

        @staticmethod
        def join(*args):
            r = '.'.join(args)
            print('os.path.join(%s): %s' % (str(args), r))
            return r


if __name__ == "__main__":
    result = []
    find_files_walk(result, 'pathdir', 'pathname')
    print('result:', result)


# UT> os.path.basename(pathname): basename.pathname
# UT> os.walk(pathdir)
# UT> fnmatch.fnmatch(file1, basename.pathname): False
# UT> fnmatch.fnmatch(file2, basename.pathname): False
# UT> fnmatch.fnmatch(basename.pathname, basename.pathname): True
# UT> os.path.join(('root', 'basename.pathname')): root.basename.pathname
# UT> result: ['root.basename.pathname']
