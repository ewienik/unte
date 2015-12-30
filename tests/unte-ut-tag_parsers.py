# UT| python2 {src_file}

from __future__ import print_function


tag_parser_definition_start = 'tag_parser_definition_start'
tag_parser_definition_end = 'tag_parser_definition_end'
tag_parser_insert_start = 'tag_parser_insert_start'
tag_parser_insert_end = 'tag_parser_insert_end'
tag_parser_exec_ignore = 'tag_parser_exec_ignore'
tag_parser_exec_check = 'tag_parser_exec_check'
tag_parser_expected = 'tag_parser_expected'


# UT[ ../unte.py * tag_parsers
TAG_PARSERS = {
    '{': tag_parser_definition_start,
    '}': tag_parser_definition_end,
    '[': tag_parser_insert_start,
    ']': tag_parser_insert_end,
    '!': tag_parser_exec_ignore,
    '|': tag_parser_exec_check,
    '>': tag_parser_expected,
}
# UT]


if __name__ == "__main__":
    print('tag_parsers:', TAG_PARSERS)


# noqa UT> tag_parsers: {'!': 'tag_parser_exec_ignore', '}': 'tag_parser_definition_end', '|': 'tag_parser_exec_check', '{': 'tag_parser_definition_start', ']': 'tag_parser_insert_end', '[': 'tag_parser_insert_start', '>': 'tag_parser_expected'}
