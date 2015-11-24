# UT| python2 {src_file}

# UT[ ../unte.py * find_files_glob
def find_files_glob(result, pathname):
    assert type(result) == list
    assert type(pathname) == str

    for path in glob.glob(pathname):
        if os.path.isfile(path):
            result.append(path)
            continue
# UT]


class os:  # noqa
    class path:  # noqa

# UT( system_iface.py * os_path_isfile
        @staticmethod
        def isfile(path):
            assert type(path) == str
# UT)

if __name__ == "__main__":
    print "Test ok"

# UT> Test wrong
# UT>
