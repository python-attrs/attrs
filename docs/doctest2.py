from __future__ import absolute_import, print_function

import sys
import sphinx
import doctest
import subprocess
import tempfile
import os
import shutil

import sphinx.ext.doctest
from sphinx.ext.doctest import (TestsetupDirective, TestcleanupDirective,
                                DoctestDirective, TestcodeDirective,
                                TestoutputDirective, DocTestBuilder)

# Path to Python 3 interpreter
python3_path = sys.executable

HERE = os.path.abspath(os.path.dirname(__file__))


class SphinxDocTestRunner(sphinx.ext.doctest.SphinxDocTestRunner):
    group_source = ''

    def reset_source(self):
        self.group_source = ''

    def run(self, test, compileflags=None, out=None, clear_globs=True):
        # add the source for this block to the group
        result = doctest.DocTestRunner.run(self, test, compileflags, out,
                                           clear_globs)
        self.group_source += ''.join(example.source
                                     for example in test.examples)
        return result


# patch the runner
sphinx.ext.doctest.SphinxDocTestRunner = SphinxDocTestRunner


class DocTest2Builder(DocTestBuilder):
    def test_group(self, group, filename):
        self.setup_runner.reset_source()
        self.test_runner.reset_source()
        self.cleanup_runner.reset_source()

        result = DocTestBuilder.test_group(self, group, filename)

        source = (self.setup_runner.group_source +
                  self.test_runner.group_source +
                  self.cleanup_runner.group_source)

        got = run_mypy(source, self.config.doctest_path)

        if got:
            test = doctest.DocTest([], {}, group.name, '', 0, None)
            example = doctest.Example('', '')
            # if not quiet:
            self.test_runner.report_failure(self._warn_out, test, example, got)
            # we hardwire no. of failures and no. of tries to 1
            self.test_runner._DocTestRunner__record_outcome(test, 1, 1)

        return result


def run_mypy(code, mypy_path):
    program = '_program.py'
    test_temp_dir = tempfile.mkdtemp()
    program_path = os.path.join(test_temp_dir, program)
    with open(program_path, 'w') as file:
        file.write(code)
    args = [
        program,
        '--hide-error-context',  # don't precede errors w/ notes about context
        '--show-traceback',
    ]
    # Type check the program.
    env = {'MYPYPATH': os.path.pathsep.join(mypy_path)}
    fixed = [python3_path, '-m', 'mypy']
    process = subprocess.Popen(fixed + args,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               env=env,
                               cwd=test_temp_dir)
    outb = process.stdout.read()
    # Split output into lines and strip the file name.
    out = []
    for line in str(outb, 'utf8').splitlines():
        parts = line.split(':', 1)
        if len(parts) == 2:
            out.append(parts[1])
        else:
            out.append(line)
    # Remove temp file.
    os.remove(program_path)
    shutil.rmtree(test_temp_dir)
    return '\n'.join(out)


def setup(app):
    app.add_directive('testsetup', TestsetupDirective)
    app.add_directive('testcleanup', TestcleanupDirective)
    app.add_directive('doctest', DoctestDirective)
    app.add_directive('testcode', TestcodeDirective)
    app.add_directive('testoutput', TestoutputDirective)
    app.add_builder(DocTest2Builder)
    # this config value adds to sys.path
    app.add_config_value('doctest_path', [], False)
    app.add_config_value('doctest_test_doctest_blocks', 'default', False)
    app.add_config_value('doctest_global_setup', '', False)
    app.add_config_value('doctest_global_cleanup', '', False)
    app.add_config_value(
        'doctest_default_flags',
        (doctest.DONT_ACCEPT_TRUE_FOR_1 |
         doctest.ELLIPSIS |
         doctest.IGNORE_EXCEPTION_DETAIL),
        False)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
