from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, List

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
    parser_build.add_argument('--live', action='store_true', help=f'Build live at {HOST}:{PORT}')
    parser_build.add_argument('--filename', type=Path, default=None, help='Explicitly specify which tex file to build')
    parser_build.add_argument('--latexmk-opt', action='append', nargs='+', type=str, help='Latexmk options')
    parser_build.set_defaults(func=_cb_parse_build)

    args = parser.parse_args()
    args.func(args)


def _cb_parse_install(args: Namespace):
    if args.from_file is not None:
        latex.install_pkg_from_file(path=args.from_file)


def _cb_parse_build(args: Namespace):
    latex.build(root=args.root,
                filename=args.filename,
                latexmk_opts=_unwrap_latexmk_opts(args.latexmk_opt))

    if args.live:
        raise NotImplementedError


def _unwrap_latexmk_opts(opts: Optional[List[List[str]]]) -> Optional[List[str]]:
    if opts is None:
        return None
    else:
        return [opt[0] for opt in opts]


if __name__ == '__main__':
    main()
