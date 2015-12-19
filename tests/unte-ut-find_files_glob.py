# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * find_files_glob
def find_files_glob(result, pathname):
    for path in glob.glob(pathname):
        if os.path.isfile(path):
            result.append(path)
            continue
# UT]


class glob:  # noqa
    @staticmethod
    def glob(path):
        print('glob.glob(%s)' % path)
        yield 'not-exist'
        yield 'exist'


class os:  # noqa
    class path:  # noqa
        @staticmethod
        def isfile(path):
            r = 'not-exist' not in path
            print('os.path.isfile(%s): %s' % (path, r))
            return r


if __name__ == "__main__":
    result = []
    find_files_glob(result, 'pathname')
    print('result:', result)


# UT> glob.glob(pathname)
# UT> os.path.isfile(not-exist): False
# UT> os.path.isfile(exist): True
# UT> result: ['exist']
