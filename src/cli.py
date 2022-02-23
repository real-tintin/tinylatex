from argparse import ArgumentParser, Namespace
from pathlib import Path

import latex

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
    parser_build.add_argument('--dvi', action='store_true', help='Build dvi')
    parser_build.add_argument('--ps', action='store_true', help='Build ps')
    parser_build.add_argument('--clean-up', action='store_true', help='Remove all temp files')
    parser_build.add_argument('--live', action='store_true', help=f'Build live at {HOST}:{PORT}')
    parser_build.add_argument('--filename', type=Path, default=None, help='Explicitly specify which tex file to build')
    parser_build.set_defaults(func=_cb_parse_build)

    args = parser.parse_args()
    args.func(args)


def _cb_parse_install(args: Namespace):
    if args.from_file is not None:
        latex.install_pkg_from_file(path=args.from_file)


def _cb_parse_build(args: Namespace):
    if args.pdf:
        latex.build(root=args.root, filename=args.filename, out_format=latex.OutFormat.Pdf)

    if args.dvi:
        latex.build(root=args.root, filename=args.filename, out_format=latex.OutFormat.Dvi)

    if args.ps:
        latex.build(root=args.root, filename=args.filename, out_format=latex.OutFormat.Ps)

    if args.clean_up:
        latex.clean_up(root=args.root)

    if args.live:
        raise NotImplementedError


if __name__ == '__main__':
    main()
