#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROJECT_ROOT="${SCRIPT_DIR}/../"

DOCKERFILE=${PROJECT_ROOT}

TMP_DIR_REL="./tmp"
TMP_DIR_ABS="${PROJECT_ROOT}/tmp"

PACKAGES_FILENAME="packages.txt"

PACKAGES_DST_REL="${TMP_DIR_REL}/${PACKAGES_FILENAME}"
PACKAGES_DST_ABS="${TMP_DIR_ABS}/${PACKAGES_FILENAME}"

IMAGE_ROOT="/tinylatex"
IMAGE_TEX_ROOT="${IMAGE_ROOT}/tex_root"

TEX_ROOT=""
BUILD_ARGS=""
PACKAGES_SRC=""

EXP_POS_ARGS=1

usage() {
  echo "Usage: tinylatex.sh TEX_ROOT [OPTIONS]

        Portable latex build environment

        Options:
        --filename              explicitly specify tex file to build (useful if more than one)
        --packages              path to packages file (default is TEX_ROOT/${PACKAGES_FILENAME})
        --build-live            use to build live and serve at localhost:8000
        --latexmk-opt=<option>  arbitrary latexmk option (can be used use multiple times)" 1>&2
}

exit_abnormal() {
  usage
  exit 1
}

windowsify_path() {
  in=$1
  echo ${in//\//\//}
}

is_windows() {
  if [[ "$(uname -s)" =~ (CYGWIN*|MINGW32*|MSYS*|MINGW*) ]]; then
    true
  else
    false
  fi
}

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --build-live)
      BUILD_ARGS="${BUILD_ARGS} --live"
      shift # past argument
      ;;
    --filename)
      shift # past argument
      BUILD_ARGS="${BUILD_ARGS} --filename $1"
      ((EXP_POS_ARGS=EXP_POS_ARGS+1))
      ;;
    --packages)
      shift # past argument
      PACKAGES_SRC=$1
      ((EXP_POS_ARGS=EXP_POS_ARGS+1))
      ;;
    --latexmk-opt=*)
      BUILD_ARGS="${BUILD_ARGS} $1"
      shift # past argument
      ;;
    -*|--*)
      exit_abnormal
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

if [ ${#POSITIONAL_ARGS[@]} -ne $EXP_POS_ARGS ]; then
  exit_abnormal
else
  TEX_ROOT=$(realpath ${POSITIONAL_ARGS[0]})
fi

if [ -z ${PACKAGES_SRC} ]; then
  PACKAGES_SRC="${TEX_ROOT}/${PACKAGES_FILENAME}"
else
  PACKAGES_SRC=$(realpath ${PACKAGES_SRC})
fi

mkdir --parents ${TMP_DIR_ABS}

if [ -f ${PACKAGES_SRC} ]; then
  cp ${PACKAGES_SRC} ${PACKAGES_DST_ABS}
else
  touch ${PACKAGES_DST_ABS}
fi

if [ is_windows ]; then
  IMAGE_ROOT="$(windowsify_path ${IMAGE_ROOT})"
  TEX_ROOT="$(windowsify_path ${TEX_ROOT})"
  PACKAGES_DST_REL="$(windowsify_path ${PACKAGES_DST_REL})"
  IMAGE_TEX_ROOT="$(windowsify_path ${IMAGE_TEX_ROOT})"
fi

docker build ${DOCKERFILE} -t tinylatex \
  --build-arg IMAGE_ROOT=${IMAGE_ROOT} \
  --build-arg PACKAGES_PATH=${PACKAGES_DST_REL}

rm -r ${TMP_DIR_ABS}

docker run -v ${TEX_ROOT}:${IMAGE_TEX_ROOT} tinylatex \
  python3 cli.py build ${IMAGE_TEX_ROOT} ${BUILD_ARGS}

exit 0
