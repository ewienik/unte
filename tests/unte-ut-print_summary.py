# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * print_summary
def print_summary(counters):
    print("\nSummary:")
    print("\tfiles for processing: %d" % counters['for_processing'])
    print("\tprocessed: %d" % counters['processed'])
    print("\tpassed: %d" % counters['passed'])
    print("\tfailed: %d" % counters['failed'])
# UT]


if __name__ == "__main__":
    print_summary({
        'for_processing': 1,
        'processed': 2,
        'passed': 3,
        'failed': 4,
    })


# UT>
# UT> Summary:
# UT> \tfiles for processing: 1
# UT> \tprocessed: 2
# UT> \tpassed: 3
# UT> \tfailed: 4
