# -*- coding: utf-8 -*-

import sys

from unittest.mock import patch, call, Mock

import nose
from nose.tools.nontrivial import raises
from nose.tools.trivial import eq_

from pydevinit import (
    _parse_args,
    _generate,
    MetadataFileGenerator
)


class Test_Main(object):

    @raises(SystemExit)
    def test_parse_failure_no_project_name(self):
        sys.argv = ['pydevinit']
        _parse_args()

    def test_parse_default(self):
        sys.argv = ['pydevinit', '-n', 'sample']
        args = _parse_args()
        eq_(args.project_name, 'sample')
        eq_(args.source_path, None)
        eq_(args.python_type, 'python')
        eq_(args.python_version, 2.7)
        eq_(args.python_interpreter, 'Default')

    def test_generate(self):
        sys.argv = ['pydevinit', '-n', 'foo', '-s', 'bar']
        args = _parse_args()
        with patch('pydevinit.MetadataFileGenerator') as mock:
            _generate(args)
            instance = mock.return_value
            calls = [
                call(
                    'project',
                    {
                        'project_name': 'foo',
                    },
                    '.project',
                ),
                call(
                    'pydevproject',
                    {
                        'source_path': 'bar',
                        'python_type': 'python',
                        'python_version': 2.7,
                        'python_interpreter': 'Default',
                    },
                    '.pydevproject',
                ),
            ]
            instance.generate.assert_has_calls(calls)


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
