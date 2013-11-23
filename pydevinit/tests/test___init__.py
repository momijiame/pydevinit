# -*- coding: utf-8 -*-

import sys
import os

try:
    from mock import patch, call, Mock
except ImportError:
    # Python 3.3+
    from unittest.mock import patch, call, Mock

import nose
from nose.tools.trivial import eq_

from pydevinit import (
    _parse_args,
    _generate,
    MetadataFileGenerator
)


class Test_Main(object):

    def test_parse_default(self):
        sys.argv = ['pydevinit']
        args = _parse_args()
        eq_(args.project_name, None)
        eq_(args.source_path, None)
        eq_(args.python_type, 'python')
        eq_(args.python_version, 2.7)
        eq_(args.python_interpreter, 'Default')

    def _test_generate(self, project_args, pydevproject_args):
        args = _parse_args()
        with patch('pydevinit.MetadataFileGenerator') as mock:
            _generate(args)
            instance = mock.return_value
            calls = [
                call('project', project_args, '.project'),
                call('pydevproject', pydevproject_args, '.pydevproject'),
            ]
            instance.generate.assert_has_calls(calls)

    def test_generate_default(self):
        sys.argv = ['pydevinit']
        project_args = {
            'project_name': os.path.split(os.getcwd())[1],
        }
        pydevproject_args = {
            'source_path': os.path.split(os.getcwd())[1],
            'python_type': 'python',
            'python_version': 2.7,
            'python_interpreter': 'Default',
        }
        self._test_generate(project_args, pydevproject_args)

    def test_generate_project_name(self):
        sys.argv = ['pydevinit', '-n', 'foo']
        project_args = {
            'project_name': 'foo',
        }
        pydevproject_args = {
            'source_path': 'foo',
            'python_type': 'python',
            'python_version': 2.7,
            'python_interpreter': 'Default',
        }
        self._test_generate(project_args, pydevproject_args)

    def test_generate_source_name(self):
        sys.argv = ['pydevinit', '-s', 'bar']
        project_args = {
            'project_name': os.path.split(os.getcwd())[1],
        }
        pydevproject_args = {
            'source_path': 'bar',
            'python_type': 'python',
            'python_version': 2.7,
            'python_interpreter': 'Default',
        }
        self._test_generate(project_args, pydevproject_args)


class Test_MetadataFileGenerator(object):

    def test_generate(self):
        with patch('jinja2.environment.Environment') as mock:
            instance = mock.return_value

            template_stream_mock = Mock()
            template_mock = Mock()
            template_mock.stream.return_value = template_stream_mock
            instance.get_template.return_value = template_mock

            generator = MetadataFileGenerator()
            generator.generate('test')

            # Environment#get_template()
            calls = [
                call('test')
            ]
            instance.get_template.assert_has_calls(calls)

            # Template#stream()
            calls = [
                call()
            ]
            template_mock.stream.assert_has_calls(calls)

            # TemplateStream#dump()
            calls = [
                call('test')
            ]
            template_stream_mock.dump.assert_has_calls(calls)

if __name__ == "__main__":
    nose.main(argv=['nosetests', '-s', '-v'], defaultTest=__file__)
