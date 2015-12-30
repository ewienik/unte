# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * enumerate_tags
def enumerate_tags(tags):
    for tag in tags['insert']:
        yield tag
# UT]


if __name__ == "__main__":
    for tag in enumerate_tags({'insert': {'t1': None, 't2': None}}):
        print(tag)


# UT> t2
# UT> t1
