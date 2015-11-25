class fnmatch:  # noqa
    # UT{ fnmatch_fnmatch
    @staticmethod
    def fnmatch(f, pattern):
        # UT= assert type(f) == str
        # UT= assert type(pattern) == str
        # UT= print('fnmatch.fnmatch(%s, %s)' % (f, pattern))
        pass
    # UT}


class glob:  # noqa
    # UT{ glob_glob
    @staticmethod
    def glob(path):
        # UT= assert type(path) == str
        # UT= print('glob.glob(%s)' % path)
        pass
    # UT}


class os:  # noqa

    # UT{ os_walk
    @staticmethod
    def walk(path):
        # UT= assert type(path) == str
        # UT= print('os.walk(%s)' % path)
        pass
    # UT}

    class path:  # noqa

        # UT{ os_path_basename
        @staticmethod
        def basename(path):
            # UT= assert type(path) == str
            # UT= print('os.path.basename(%s)' % path)
            pass
        # UT}

        # UT{ os_path_isdir
        @staticmethod
        def isdir(path):
            # UT= assert type(path) == str
            # UT= print('os.path.isdir(%s)' % path)
            pass
        # UT}

        # UT{ os_path_isfile
        @staticmethod
        def isfile(path):
            # UT= assert type(path) == str
            # UT= print('os.path.isfile(%s)' % path)
            pass
        # UT}

        # UT{ os_path_join
        @staticmethod
        def join(*args):
            # UT= for arg in args:
            # UT=     assert type(arg) == str
            # UT= print('os.path.join(%s)' % str(args))
            pass
        # UT}
