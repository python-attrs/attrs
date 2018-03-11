# this file is adapted from mypy.test.testcmdline

import os
import re
import subprocess
import sys

from tests.mypy_pytest_plugin import (
    DataSuite, assert_string_arrays_equal, normalize_error_messages
)


pytest_plugins = ['tests.mypy_pytest_plugin']

# Path to Python 3 interpreter
python3_path = sys.executable
test_temp_dir = 'tmp'
this_dir = os.path.dirname(os.path.realpath(__file__))
test_file = os.path.join(this_dir, 'mypy.tests.py')
prefix_dir = os.path.join(os.path.dirname(this_dir), 'src')


class PythonEvaluationSuite(DataSuite):
    files = [test_file]
    base_path = test_temp_dir
    optional_out = True
    native_sep = True

    def run_case(self, testcase):
        _test_python_evaluation(testcase)


def _test_python_evaluation(testcase):
    assert testcase.old_cwd is not None, "test was not properly set up"
    # Write the program to a file.
    # we omit .py extension to be compatible with called to
    # expand_errors parse_test_cases.
    program = 'main'
    program_path = os.path.join(test_temp_dir, program)
    with open(program_path, 'w') as file:
        for s in testcase.input:
            file.write('{}\n'.format(s))

    args = parse_args(testcase.input[0])
    args.append('--show-traceback')
    # Type check the program.
    fixed = [python3_path, '-m', 'mypy', program]
    process = subprocess.Popen(fixed + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               env={'MYPYPATH': prefix_dir},
                               cwd=test_temp_dir)
    outb, errb = process.communicate()
    # Split output into lines.
    out = [s.rstrip('\n\r') for s in str(outb, 'utf8').splitlines()]
    # Remove temp file.
    os.remove(program_path)
    # Compare actual output to expected.
    out = normalize_error_messages(out)
    assert_string_arrays_equal(testcase.output, out,
                               'Invalid output ({}, line {})'.format(
                                   testcase.file, testcase.line))


def parse_args(line):
    """Parse the first line of the program for the command line.

    This should have the form

      # cmd: mypy <options>

    For example:

      # cmd: mypy pkg/
    """
    m = re.match('# cmd: mypy (.*)$', line)
    if not m:
        return []  # No args
    return m.group(1).split()
