# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * find_files_glob
def find_files_glob(result, pathname):
    assert type(result) == list
    assert type(pathname) == str
    print('find_files_glob(%s, %s)' % (result, pathname))

    for path in glob.glob(pathname):
        if os.path.isfile(path):
            result.append(path)
            continue
# UT]


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
    class path:  # noqa

        # UT( externals.py * os_path_isfile
        @staticmethod
        def isfile(path):
            assert type(path) == str
            print('os.path.isfile(%s)' % path)
        # UT)
            r = 'not-exist' not in path
            print('return %s' % r)
            return r


if __name__ == "__main__":
    find_files_glob([], 'pathname')


# UT> find_files_glob([], pathname)
# UT> glob.glob(pathname)
# UT> os.path.isfile(not-exist)
# UT> return False
# UT> os.path.isfile(exist)
# UT> return True
