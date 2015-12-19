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


def tag_get(line):
    match = PROG_TAG.match(line)
    if match is not None:
        return match.group(1), match.group(2)
    return None, None


def tag_parse(tags, tag_type, tag_value, line_no, path_dir):
    if tag_type not in TAG_PARSERS:
        return "Unknown tag type '%s'" % tag_type
    return TAG_PARSERS[tag_type](tags, tag_value, line_no, path_dir)


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


def tag_parser_definition_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    stack = tags['current']['definition']
    if len(stack) == 0:
        return "End tag without starting tag"
    stack.pop()['end'] = line_no


def tag_parser_exec_check(tags, value, line_no, path_dir):
    cmd = value.strip()
    if len(cmd) == 0:
        return "Should be a command."
    tags['exec'].append({'check': True, 'cmd': cmd})


def tag_parser_exec_ignore(tags, value, line_no, path_dir):
    cmd = value.strip()
    if len(cmd) == 0:
        return "Should be a command."
    tags['exec'].append({'check': False, 'cmd': cmd})


def tag_parser_expected(tags, value, line_no, path_dir):
    tags['expected'].append(value + '\n')


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


def tag_parser_insert_end(tags, value, line_no, path_dir):
    if len(value.strip()) != 0:
        return "Wrong args for tag. There should be no args."
    tag = tags['current']['insert']
    if not tag:
        return "End tag without starting tag"
    tag['end'] = line_no
    tags['current']['insert'] = None


TAG_PARSERS = {
    '{': tag_parser_definition_start,
    '}': tag_parser_definition_end,
    '[': tag_parser_insert_start,
    ']': tag_parser_insert_end,
    '!': tag_parser_exec_ignore,
    '|': tag_parser_exec_check,
    '>': tag_parser_expected,
}


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


def enumerate_tags(tags):
    for tag in tags['insert']:
        yield tag


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


def update_file(path, tags):
    tags_db = dict([
        [tag['file'], extract_tags(tag['file'])]
        for tag in tags['insert']
    ])

    temp_dst = tempfile.TemporaryFile(mode='w+')
    compile_file(temp_dst, path, tags, tags_db)
    temp_dst.seek(0)
    shutil.copyfileobj(temp_dst, open(path, 'w'))


def diff_file(path, tags, output):
    ok = True
    diff = []
    for line in difflib.context_diff(
        tags['expected'], output, fromfile='EXPECTED', tofile='OUTPUT',
    ):
        ok = False
        diff.append(line)

    if not ok:
        print('\n%s:1:error:There is unexpected ouput' % path)
        for line in diff:
            sys.stdout.write(line)
        return False

    return True


def execute_file(path, tags):
    if len(tags['exec']) == 0:
        print('\n%s:1:error:There are no execute tags' % path)
        return False
    env = dict(os.environ)
    tempdir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(tempdir)

    result = True
    output = ''
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
            output += e.output
            if exe['check']:
                check += e.output.splitlines(True)
            print(output)
            result = False
            break
        output += out
        if exe['check']:
            check += out.splitlines(True)

    os.chdir(cwd)
    shutil.rmtree(tempdir)

    return result, check


# UT{ parse_args
def parse_args():
    parser = argparse.ArgumentParser(description='Process unit tests')
    parser.add_argument()
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
        if not status or not diff_file(path, tags, output):
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
    if len(sys.argv) < 2:
        print('Error: there should be arguments')
        sys.exit(1)

    paths = find_files(sys.argv[1:])
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
