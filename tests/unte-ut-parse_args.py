# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * parse_args
def parse_args():
    parser = argparse.ArgumentParser(description='Process unit tests')
    parser.add_argument('paths', nargs='+')
    return parser.parse_args()
# UT]


class argparse:  # noqa
    class ArgumentParser:
        id = 0

        def __init__(self, **kwargs):
            self.id = argparse.ArgumentParser.id
            argparse.ArgumentParser.id += 1
            print('argparse.ArgumentParser.__init__(%d, %s)' % (
                self.id, str(kwargs)
            ))

        def add_argument(self, *args, **kwargs):
            print('argparse.ArgumentParser.add_argument(%d, %s, %s)' % (
                self.id, str(args), str(kwargs)
            ))

        def parse_args(self):
            r = 'parse_args'
            print('argparse.ArgumentParser.parse_args(%d): %s' % (self.id, r))
            return r


if __name__ == "__main__":
    result = parse_args()
    print('result:', result)


# noqa UT> argparse.ArgumentParser.__init__(0, {'description': 'Process unit tests'})
# UT> argparse.ArgumentParser.add_argument(0, ('paths',), {'nargs': '+'})
# UT> argparse.ArgumentParser.parse_args(0): parse_args
# UT> result: parse_args
