# this file is adapted from mypy.test.testcmdline

import os
import re
import subprocess
import sys

from mypy.test.data import parse_test_cases, DataSuite
from mypy.test.helpers import (assert_string_arrays_equal,
                               normalize_error_messages)

pytest_plugins = ['mypy.test.data']

# Path to Python 3 interpreter
python3_path = sys.executable
test_temp_dir = 'tmp'
test_file = os.path.splitext(os.path.realpath(__file__))[0] + '.test'
prefix_dir = os.path.join(os.path.dirname(os.path.dirname(test_file)), 'src')


class PythonEvaluationSuite(DataSuite):

    @classmethod
    def cases(cls):
        return parse_test_cases(test_file,
                                _test_python_evaluation,
                                base_path=test_temp_dir,
                                optional_out=True,
                                native_sep=True)

    def run_case(self, testcase):
        _test_python_evaluation(testcase)


def _test_python_evaluation(testcase):
    assert testcase.old_cwd is not None, "test was not properly set up"
    # Write the program to a file.
    program = '_program.py'
    program_path = os.path.join(test_temp_dir, program)
    with open(program_path, 'w') as file:
        for s in testcase.input:
            file.write('{}\n'.format(s))
    args = parse_args(testcase.input[0])
    args.append('--show-traceback')
    # Type check the program.
    fixed = [python3_path, '-m', 'mypy']
    process = subprocess.Popen(fixed + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               env={'MYPYPATH': prefix_dir},
                               cwd=test_temp_dir)
    outb = process.stdout.read()
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
        return []  # No args; mypy will spit out an error.
    return m.group(1).split()
