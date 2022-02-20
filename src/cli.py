from argparse import ArgumentParser, Namespace
from pathlib import Path

import tex_live

HOST = 'localhost'
PORT = 8000


def main():
    parser = ArgumentParser(description='The tinylatex cli')
    subparsers = parser.add_subparsers(help='COMMAND help')

    parser_install = subparsers.add_parser('install', help='install help')
    parser_install.add_argument('--from-file', type=Path, default=None, help='Install latex packages from file')
    parser_install.set_defaults(func=_cb_parse_install)

    parser_build = subparsers.add_parser('build', help='build help')
    parser_build.add_argument('root', type=Path, help='Path to latex project root')
    parser_build.add_argument('--pdf', action='store_true', help='Build pdf')
    parser_build.add_argument('--live', action='store_true', help=f'Build live at {HOST}:{PORT}')
    parser_build.add_argument('--filename', type=Path, default=None, help='Explicitly specify which tex file to build')
    parser_build.set_defaults(func=_cb_parse_build)

    args = parser.parse_args()
    args.func(args)


def _cb_parse_install(args: Namespace):
    if args.from_file is not None:
        tex_live.install_pkg_from_file(path=args.from_file)


def _cb_parse_build(args: Namespace):
    if args.pdf:
        tex_live.build_pdf(root=args.root, filename=args.filename)

    if args.live:
        raise NotImplementedError


if __name__ == '__main__':
    main()
