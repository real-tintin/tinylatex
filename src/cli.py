import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, List

import config_reader
import font
import latex
import live_pdf
from builder import Builder
from file_watcher import FileWatcher

HOST = '0.0.0.0'
PORT = 8000

logging.basicConfig(level=logging.INFO)


def main():
    parser = ArgumentParser(description='The tinylatex cli')
    subparsers = parser.add_subparsers(help='COMMAND help')

    parser_install = subparsers.add_parser('config', help='config help')
    parser_install.add_argument('path', type=Path, help='Path to config file to setup env')
    parser_install.set_defaults(func=_cb_parse_config_args)

    parser_build = subparsers.add_parser('build', help='build help')
    parser_build.add_argument('root', type=Path, help='Path to latex project root')
    parser_build.add_argument('--live-pdf', action='store_true', help=f'Build live pdf at {HOST}:{PORT}')
    parser_build.add_argument('--main', type=Path, default=None, help='Explicitly specify main tex file to build')
    parser_build.add_argument('--latexmk-opt', action='append', nargs='+', type=str, help='Latexmk options')
    parser_build.set_defaults(func=_cb_parse_build_args)

    args = parser.parse_args()
    args.func(args)


def _cb_parse_config_args(args: Namespace):
    config = config_reader.from_file(path=args.path)

    latex.install_packages(packages=config.packages)
    font.download(fonts=config.fonts)


def _cb_parse_build_args(args: Namespace):
    builder = Builder(root=args.root,
                      main=args.main,
                      latexmk_opts=_unwrap_latexmk_opts(args.latexmk_opt))

    if args.live_pdf:
        watcher = FileWatcher(root=args.root, cb=builder.build, globs=['*.tex', '*.eps', '*.png', '*.jpg'])
        watcher.start()

        live_pdf.launch(host=HOST,
                        port=PORT,
                        pdf_path=builder.get_tex_path().with_suffix('.pdf'),  # Note, pdf output is assumed
                        get_version_cb=builder.get_version)

    else:
        builder.build()


def _unwrap_latexmk_opts(opts: Optional[List[List[str]]]) -> Optional[List[str]]:
    if opts is None:
        return None
    else:
        return [opt[0] for opt in opts]


if __name__ == '__main__':
    main()
