# unte

Unit testing tool for all languages (C, C++, python, golang, javascript, java,
...). You can name fragments of source code and prepare tests for them in
separate files. Tagged parts of files will be automatically included in test
files, which you can run with your tool (you can run tests directly with
interpreter or compile it before; test will be run in temporary directory).
Your test will produce stdout or stderr which will be diffied with expected
output and the result of diff will be a result of test.

# Command line options

Run simple `unte.py paths...` where paths could be a direct paths of tests or
glob paths (you can use `*` or `**` globs)
