# Tinylatex

Tinylatex is a tiny portable (containerized) latex build environment. This is simply
accomplished by using the following existing tools:

* TeX Live Docker image [minidocks/texlive](https://github.com/minidocks/texlive)
* TeX Live tools (such as ``tlmgr`` and ``pdflatex``)

## Usage

```shell
./tinylatex.sh ./example --filename main.tex
```

Use ``./tinylatex.sh --help`` for further details.

## Packages
Besides the standard latex packages, one can install additional packages by adding them to
a *packages.txt*, see example for details.
