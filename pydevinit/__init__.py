#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader


class MetadataFileGenerator(object):

    def __init__(self, package_name='pydevinit', template_dir='templates'):
        loader = PackageLoader(package_name, template_dir)
        self.environ = Environment(loader=loader)

    def generate(self, template_name, args={}, file_name=None):
        template = self.environ.get_template(template_name)
        template_stream = template.stream(**args)
        template_stream.dump(file_name or template_name)


def _parse_args():
    description = 'Eclipse PyDev Plugin Project Initialize Script'
    option_n_help = 'Set project name'
    option_s_help = 'Set project source path'
    option_t_help = 'Set python type (default: python)'
    option_v_help = 'Set python version (default: 2.7)'
    option_i_help = 'Set python interpreter (default: Default)'

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument(
        '-n', '--project-name',
        type=str,
        required=True,
        help=option_n_help,
    )
    arg_parser.add_argument(
        '-s', '--source-path',
        type=str,
        default=None,
        help=option_s_help,
    )
    arg_parser.add_argument(
        '-t', '--python-type',
        type=str,
        default='python',
        help=option_t_help,
    )
    arg_parser.add_argument(
        '-v', '--python-version',
        type=float,
        default='2.7',
        help=option_v_help,
    )
    arg_parser.add_argument(
        '-i', '--python-interpreter',
        type=str,
        default='Default',
        help=option_i_help,
    )

    return arg_parser.parse_args()


def _generate(args):
    generator = MetadataFileGenerator()

    # .project
    gen_args = {
        'project_name': args.project_name,
    }
    generator.generate('project', gen_args, '.project')

    # .pydevproject
    gen_args = {
        'source_path': args.source_path or args.project_name,
        'python_type': args.python_type,
        'python_version': args.python_version,
        'python_interpreter': args.python_interpreter,
    }
    generator.generate('pydevproject', gen_args, '.pydevproject')


def main():
    args = _parse_args()
    _generate(args)

if __name__ == '__main__':
    main()
