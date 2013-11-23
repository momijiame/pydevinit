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
        pydevproj_template = self.environ.get_template(template_name)
        pydevproj_template.stream(**args).dump(file_name or template_name)


def main():
    description = 'Eclipse PyDev Plugin Project Initialize Script'
    option_s_help = 'Set project source path'
    option_t_help = 'Set python type (default: python)'
    option_v_help = 'Set python version (default: 2.7)'
    option_i_help = 'Set python interpreter (default: Default)'

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument(
        '-s', '--source-path',
        type=str,
        required=True,
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

    args = arg_parser.parse_args()

    generator = MetadataFileGenerator()

    # .pydevproject
    gen_args = {
        'source_path': args.source_path,
        'python_type': args.python_type,
        'python_version': args.python_version,
        'python_interpreter': args.python_interpreter,
    }
    generator.generate('pydevproject', gen_args, '.pydevproject')

    # .project
    generator.generate('project', gen_args, '.project')

if __name__ == '__main__':
    main()
