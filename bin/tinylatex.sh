#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

PROJECT_ROOT="${SCRIPT_DIR}/../"

DOCKERFILE=${PROJECT_ROOT}

TMP_DIR_REL="./tmp"
TMP_DIR_ABS="${PROJECT_ROOT}/tmp"

CONFIG_FILENAME="config.json"

CONFIG_DST_REL="${TMP_DIR_REL}/${CONFIG_FILENAME}"
CONFIG_DST_ABS="${TMP_DIR_ABS}/${CONFIG_FILENAME}"

IMAGE_ROOT="/tinylatex"
IMAGE_TEX_ROOT="${IMAGE_ROOT}/tex_root"

TEX_ROOT=""
BUILD_ARGS=""
CONFIG_SRC=""

EXP_POS_ARGS=1

usage() {
  echo "Usage: tinylatex.sh TEX_ROOT [OPTIONS]

        Portable latex build environment

        Options:
        --main                  explicitly specify main tex file to build (useful if more than one)
        --config                path to config file (default search path TEX_ROOT/${CONFIG_FILENAME})
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
    --main)
      shift # past argument
      BUILD_ARGS="${BUILD_ARGS} --main $1"
      ((EXP_POS_ARGS=EXP_POS_ARGS+1))
      ;;
    --config)
      shift # past argument
      CONFIG_SRC=$1
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

if [ -z ${CONFIG_SRC} ]; then
  CONFIG_SRC="${TEX_ROOT}/${CONFIG_FILENAME}"
else
  CONFIG_SRC=$(realpath ${CONFIG_SRC})
fi

mkdir --parents ${TMP_DIR_ABS}

if [ -f ${CONFIG_SRC} ]; then
  cp ${CONFIG_SRC} ${CONFIG_DST_ABS}
else
  touch ${CONFIG_DST_ABS}
fi

if [ is_windows ]; then
  IMAGE_ROOT="$(windowsify_path ${IMAGE_ROOT})"
  TEX_ROOT="$(windowsify_path ${TEX_ROOT})"
  CONFIG_DST_REL="$(windowsify_path ${CONFIG_DST_REL})"
  IMAGE_TEX_ROOT="$(windowsify_path ${IMAGE_TEX_ROOT})"
fi

docker build ${DOCKERFILE} -t tinylatex \
  --build-arg IMAGE_ROOT=${IMAGE_ROOT} \
  --build-arg CONFIG_FROM=${CONFIG_DST_REL}

rm -r ${TMP_DIR_ABS}

docker run -v ${TEX_ROOT}:${IMAGE_TEX_ROOT} tinylatex \
  python3 cli.py build ${IMAGE_TEX_ROOT} ${BUILD_ARGS}

exit 0
