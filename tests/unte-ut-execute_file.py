# UT| python2 {src_file}

from __future__ import print_function


# UT[ ../unte.py * execute_file
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
# UT]


class os:  # noqa
    environ = {'env': 'env'}

    @staticmethod
    def chdir(path):
        print('os.chdir(%s)' % path)

    @staticmethod
    def getcwd():
        r = 'cwd'
        print('os.getcwd(): %s' % r)
        return r

    class path:  # noqa
        @staticmethod
        def join(*args):
            r = '.'.join(args)
            print('os.path.join(%s): %s' % (str(args), r))
            return r


class shutil:  # noqa
    @staticmethod
    def rmtree(path):
        print('shutil.rmtree(%s)' % path)


class subprocess:  # noqa
    STDOUT = 'stdout'
    run_failed = True

    @staticmethod
    def check_output(cmd, **kwargs):
        if subprocess.run_failed:
            r = 'Exception'
        else:
            r = 'output.' + cmd
        print('subprocess.check_output(%s, %s): %s' % (cmd, str(kwargs), r))
        if subprocess.run_failed:
            raise subprocess.CalledProcessError()
        return r

    class CalledProcessError:
        output = 'call error'

        def __str__(self):
            return 'call exception'


class tempfile:  # noqa
    @staticmethod
    def mkdtemp():
        r = 'tempdir'
        print('tempfile.mkdtemp(): %s' % r)
        return r


if __name__ == "__main__":
    tags = {'exec': []}
    result, check = execute_file('path', tags)
    print('result:', result, check)
    tags['exec'] = [{'cmd': '{env_wrong}'}]
    result, check = execute_file('path', tags)
    print('result:', result, check)
    tags['exec'] = [{'cmd': '{src_file}', 'check': False}]
    result, check = execute_file('path', tags)
    print('result:', result, check)
    tags['exec'] = [{'cmd': '{src_file}', 'check': True}]
    result, check = execute_file('path', tags)
    print('result:', result, check)
    subprocess.run_failed = False
    tags['exec'] = [{'cmd': '{src_file}', 'check': False}]
    result, check = execute_file('path', tags)
    print('result:', result, check)
    tags['exec'] = [{'cmd': '{src_file}', 'check': True}]
    result, check = execute_file('path', tags)
    print('result:', result, check)


# UT>
# UT> path:1:error:There are no execute tags
# UT> result: False []
# UT> tempfile.mkdtemp(): tempdir
# UT> os.getcwd(): cwd
# UT> os.chdir(tempdir)
# UT> os.path.join(('cwd', 'path')): cwd.path
# UT>
# UT> path:1:error:Unknown key "\'env_wrong\'" in "{env_wrong}"
# UT> os.chdir(cwd)
# UT> shutil.rmtree(tempdir)
# UT> result: False []
# UT> tempfile.mkdtemp(): tempdir
# UT> os.getcwd(): cwd
# UT> os.chdir(tempdir)
# UT> os.path.join(('cwd', 'path')): cwd.path
# noqa UT> subprocess.check_output(cwd.path, {'shell': True, 'stderr': 'stdout'}): Exception
# UT>
# UT> path:1:error:call exception
# UT>
# UT> call error
# UT> os.chdir(cwd)
# UT> shutil.rmtree(tempdir)
# UT> result: False []
# UT> tempfile.mkdtemp(): tempdir
# UT> os.getcwd(): cwd
# UT> os.chdir(tempdir)
# UT> os.path.join(('cwd', 'path')): cwd.path
# noqa UT> subprocess.check_output(cwd.path, {'shell': True, 'stderr': 'stdout'}): Exception
# UT>
# UT> path:1:error:call exception
# UT>
# UT> call error
# UT> os.chdir(cwd)
# UT> shutil.rmtree(tempdir)
# UT> result: False [u'call error']
# UT> tempfile.mkdtemp(): tempdir
# UT> os.getcwd(): cwd
# UT> os.chdir(tempdir)
# UT> os.path.join(('cwd', 'path')): cwd.path
# noqa UT> subprocess.check_output(cwd.path, {'shell': True, 'stderr': 'stdout'}): output.cwd.path
# UT> os.chdir(cwd)
# UT> shutil.rmtree(tempdir)
# UT> result: True []
# UT> tempfile.mkdtemp(): tempdir
# UT> os.getcwd(): cwd
# UT> os.chdir(tempdir)
# UT> os.path.join(('cwd', 'path')): cwd.path
# noqa UT> subprocess.check_output(cwd.path, {'shell': True, 'stderr': 'stdout'}): output.cwd.path
# UT> os.chdir(cwd)
# UT> shutil.rmtree(tempdir)
# UT> result: True [u'output.cwd.path']
