# Tinylatex

Tinylatex is a tiny portable (containerized) latex build environment. This is simply
accomplished by using the following existing tools:

* TeX Live Docker image [minidocks/texlive](https://github.com/minidocks/texlive)
* [TinyTex](https://yihui.org/tinytex/) (small LaTeX distribution based on TeX Live)

## Installation
Simply clone this repository and add */path/to/repo/bin* to your ``PATH``.

## Usage
Example:

```shell
tinylatex.sh /path/to/repo/example --main main.tex --latexmk-opt=-pdflua
```

Use ``tinylatex.sh --help`` to list all options.

## Config
The build environment can be configured by adding a *config.json*. Current features:

* Additional latex packages to install
* Fonts to download and install

See example for details.
