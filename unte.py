#!/usr/bin/env python

from __future__ import print_function

LICENSE = """
The MIT License (MIT)

Copyright (c) 2015 ewienik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import difflib
import fnmatch
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback

PROG_TAG = re.compile('.*UT([!|\[\]{}>])\s(.*)$')


# UT{ find_files
def find_files(globs):
    result = []

    for pathname in globs:
        path_dir, sep, path_file = pathname.partition('**')
        if len(sep) == 0:
            find_files_glob(result, pathname)
            continue

        if len(path_dir) == 0 or os.path.isdir(path_dir):
            find_files_walk(result, path_dir, path_file)

    return result
# UT}


# UT{ find_files_glob
def find_files_glob(result, pathname):
    for path in glob.glob(pathname):
        if os.path.isfile(path):
            result.append(path)
            continue
# UT}


# UT{ find_files_walk
def find_files_walk(result, path_dir, path_file):
    pattern = os.path.basename(path_file)
    for root, dirs, files in os.walk(path_dir):
        for f in files:
            if fnmatch.fnmatch(f, pattern):
                result.append(os.path.join(root, f))
# UT}


# UT{ tag_get
def tag_get(line):
    match = PROG_TAG.match(line)
    if match is not None:
        return match.group(1), match.group(2)
    return None, None
# UT}


# UT{ tag_parse
def tag_parse(tags, tag_type, tag_value, line_no, path_dir):
    if tag_type not in TAG_PARSERS:
        return "Unknown tag type '%s'" % tag_type
    return TAG_PARSERS[tag_type](tags, tag_value, line_no, path_dir)
# UT}


# UT{ tag_parser_definition_start
def tag_parser_definition_start(tags, value, line_no, path_dir):
    name = value.strip()
    if len(name) == 0:
        return "There is no a tag name."
    if name in tags['definition']:
        return "Duplicate start of tag '%s' (previous at %d)" % (
            name, tags['definition'][name]['start']
        )
    tag = {'start': line_no, 'end': None}
    tags['definition'][name] = tag
    tags['current']['definition'].append(tag)
# UT}


# UT{ tag_parser_definition_end
def tag_parser_definition_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    stack = tags['current']['definition']
    if len(stack) == 0:
        return "End tag without starting tag"
    stack.pop()['end'] = line_no
# UT}


# UT{ tag_parser_exec_check
def tag_parser_exec_check(tags, value, line_no, path_dir):
    cmd = value.strip()
    if len(cmd) == 0:
        return "Should be a command."
    tags['exec'].append({'check': True, 'cmd': cmd})
# UT}


# UT{ tag_parser_exec_ignore
def tag_parser_exec_ignore(tags, value, line_no, path_dir):
    cmd = value.strip()
    if len(cmd) == 0:
        return "Should be a command."
    tags['exec'].append({'check': False, 'cmd': cmd})
# UT}


# UT{ tag_parser_expected
def tag_parser_expected(tags, value, line_no, path_dir):
    line = value + '\n'
    if sys.version_info < (3, 0):
        line = unicode(line)
    tags['expected'].append(line)
# UT}


# UT{ tag_parser_insert_start
def tag_parser_insert_start(tags, value, line_no, path_dir):
    outer = tags['current']['insert']
    if outer:
        return "Tag inside other (outer defined in line %d)." % outer['start']

    args = value.split('*')
    if len(args) != 2:
        return "There should be two args: a path and a tag name."
    path = args[0].strip()
    if len(path) == 0:
        return "Path arg is empty."
    name = args[1].strip()
    if len(name) == 0:
        return "Tag name arg is empty."

    tag = {
        'name': name,
        'file': os.path.join(path_dir, path),
        'start': line_no,
        'end': None,
    }
    tags['insert'].append(tag)
    tags['current']['insert'] = tag
# UT}


# UT{ tag_parser_insert_end
def tag_parser_insert_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    tag = tags['current']['insert']
    if not tag:
        return "End tag without starting tag"
    tag['end'] = line_no
    tags['current']['insert'] = None
# UT}


# UT{ tag_parsers
TAG_PARSERS = {
    '{': tag_parser_definition_start,
    '}': tag_parser_definition_end,
    '[': tag_parser_insert_start,
    ']': tag_parser_insert_end,
    '!': tag_parser_exec_ignore,
    '|': tag_parser_exec_check,
    '>': tag_parser_expected,
}
# UT}


# UT{ extract_tags
def extract_tags(path):
    tags = {
        'current': {
            'definition': [],
            'insert': None,
        },
        'definition': {},
        'insert': [],
        'assert': [],
        'exec': [],
        'expected': [],
    }

    ok = True
    f = open(path)
    line_no = 0
    path_dir = os.path.dirname(path)
    for line in f:
        line_no += 1

        tag_type, tag_value = tag_get(line)
        if tag_type is None or tag_value is None:
            continue
        err = tag_parse(tags, tag_type, tag_value, line_no, path_dir)
        if err:
            print('\n%s:%d:error:%s' % (path, line_no, err), end='')
            ok = False

    if not ok:
        print('')
        sys.exit(1)

    return tags
# UT}


# UT{ write_part_file_one
def write_part_file_one(dst, src, start, end):
    f = open(src)
    line_no = 0
    state = 'normal'
    for line in f:
        line_no += 1
        if state == 'inside':
            if end == line_no:
                return
            dst.write(line)
            continue
        if start == line_no:
            state = 'inside'
# UT}


# UT{ write_part_file
def write_part_file(dst, tags, tag_path, tag_name):
    if tag_path not in tags:
        return
    definition = tags[tag_path]['definition']
    tag_child = definition.get(tag_name)
    if tag_child:
        write_part_file_one(
            dst, tag_path,
            tag_child['start'], tag_child['end']
        )
# UT}


# UT{ enumerate_tags
def enumerate_tags(tags):
    for tag in tags['insert']:
        yield tag
# UT}


# UT{ compile_file
def compile_file(dst, src, tags_master, tags_db):
    f = open(src)
    tag_iter = iter(enumerate_tags(tags_master))
    try:
        tag = next(tag_iter)
    except StopIteration:
        tag = None
    line_no = 0
    inside_tag = False
    for line in f:
        line_no += 1
        if inside_tag and tag['end'] == line_no:
            inside_tag = False
            try:
                tag = next(tag_iter)
            except StopIteration:
                tag = None
        if inside_tag:
            continue
        dst.write(line)
        if tag is not None and tag['start'] == line_no:
            inside_tag = True
            write_part_file(dst, tags_db, tag['file'], tag['name'])
# UT}


# UT{ update_file
def update_file(path, tags):
    tags_db = dict([
        [tag['file'], extract_tags(tag['file'])]
        for tag in tags['insert']
    ])

    temp_dst = tempfile.TemporaryFile(mode='w+')
    compile_file(temp_dst, path, tags, tags_db)
    temp_dst.seek(0)
    shutil.copyfileobj(temp_dst, open(path, 'w'))
# UT}


# UT{ diff_file
def diff_file(path, tags, output):
    ok = True
    diff = []
    for line in difflib.context_diff(
        tags['expected'], output, fromfile='EXPECTED', tofile='OUTPUT',
    ):
        ok = False
        diff.append(line)

    if not ok:
        print('\n%s:1:error:There is unexpected output' % path)
        for line in diff:
            sys.stdout.write(line)
        return False

    return True
# UT}


# UT{ escape_lines
def escape_lines(lines):
    i = 0
    start = 2 if sys.version_info < (3, 0) else 1
    while i < len(lines):
        line = lines[i]
        if len(line) == 0:
            i += 1
            continue
        if line[-1] == '\n':
            line = line[:-1]
        line = repr(line)[start:-1] + '\n'
        lines[i] = line
        i += 1
# UT}


# UT{ execute_file
def execute_file(path, tags):
    if len(tags['exec']) == 0:
        print('\n%s:1:error:There are no execute tags' % path)
        return False, []
    env = dict(os.environ)
    tempdir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tempdir)

    result = True
    output = u''
    check = []
    for exe in tags['exec']:
        env['src_file'] = os.path.join(cwd, path)
        try:
            cmd = exe['cmd'].format(**env)
        except KeyError as e:
            print('\n%s:1:error:Unknown key "%s" in "%s"' % (
                path, e, exe['cmd']
            ))
            result = False
            break

        try:
            out = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True
            )
        except subprocess.CalledProcessError as e:
            print('\n%s:1:error:%s\n' % (path, e))
            decoded = e.output.decode('utf-8')
            output += decoded
            if exe['check']:
                check += decoded.splitlines(True)
            print(output)
            result = False
            break
        decoded = out.decode('utf-8')
        output += decoded
        if exe['check']:
            check += decoded.splitlines(True)

    os.chdir(cwd)
    shutil.rmtree(tempdir)

    return result, check
# UT}


# UT{ parse_args
def parse_args():
    parser = argparse.ArgumentParser(description='Process unit tests')
    parser.add_argument('paths', nargs='+')
    return parser.parse_args()
# UT}


# UT{ print_summary
def print_summary(counters):
    print("\nSummary:")
    print("\tfiles for processing: %d" % counters['for_processing'])
    print("\tprocessed: %d" % counters['processed'])
    print("\tpassed: %d" % counters['passed'])
    print("\tfailed: %d" % counters['failed'])
# UT}


# UT{ process_file
def process_file(path, counters):
    ok = True
    counters['processed'] += 1
    print('\rProcessing %d/%d file ... ' % (
        counters['processed'], counters['for_processing']
    ), end='')
    sys.stdout.flush()
    try:
        tags = extract_tags(path)
        update_file(path, tags)
        status, output = execute_file(path, tags)
        if not status:
            ok = False
        else:
            escape_lines(output)
            if not diff_file(path, tags, output):
                ok = False
    except:
        ok = False
        traceback.print_exc()
    if ok:
        counters['passed'] += 1
    else:
        counters['failed'] += 1
        print('Error in', path)

    return ok
# UT}


# UT{ main
def main():
    args = parse_args()
    paths = find_files(args.paths)

    counters = {
        'for_processing': len(paths),
        'processed': 0,
        'passed': 0,
        'failed': 0,
    }

    result = 0
    for path in paths:
        if not process_file(path, counters):
            result = 1

    print_summary(counters)
    sys.exit(result)
# UT}


if __name__ == '__main__':
    main()
