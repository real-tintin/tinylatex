#!/bin/bash

# TODO: Refactor.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

TMP_DIR_REL="./tmp"
TMP_DIR_ABS="${SCRIPT_DIR}/tmp"

PACKAGES_FILENAME="packages.txt"

PACKAGES_DST_REL="${TMP_DIR_REL}/${PACKAGES_FILENAME}"
PACKAGES_DST_ABS="${TMP_DIR_ABS}/${PACKAGES_FILENAME}"

IMAGE_ROOT="/tinylatex"
IMAGE_TEX_ROOT="${IMAGE_ROOT}/tex_root"

TEX_ROOT=$(realpath $1)
PACKAGES_SRC="${TEX_ROOT}/${PACKAGES_FILENAME}"

echo $TEX_ROOT

if [ -d "${TEX_ROOT}" ]; then
  BUILD_ARGS="${IMAGE_TEX_ROOT} ${@:2}"
else
  BUILD_ARGS="${@:1}" # TODO: run help container? and exit
fi

windowsify_path() {
  in=$1
  echo ${in//\//\//}
}

create_and_populate_tmp_dir() {
  mkdir --parents ${TMP_DIR_ABS}
  cp ${PACKAGES_SRC} ${PACKAGES_DST_ABS}
}

remove_tmp_dir() {
  rm -r ${TMP_DIR_ABS}
}

create_and_populate_tmp_dir

if [[ "$(uname -s)" =~ (CYGWIN*|MINGW32*|MSYS*|MINGW*) ]]; then
  IMAGE_ROOT="$(windowsify_path ${IMAGE_ROOT})"
  TEX_ROOT="$(windowsify_path ${TEX_ROOT})"
  PACKAGES_DST_REL="$(windowsify_path ${PACKAGES_DST_REL})"
  IMAGE_TEX_ROOT="$(windowsify_path ${IMAGE_TEX_ROOT})"
fi

echo $IMAGE_ROOT
echo $TEX_ROOT
echo $PACKAGES_DST_REL
echo $IMAGE_TEX_ROOT

exit 1

docker build ${SCRIPT_DIR} -t tinylatex \
  --build-arg IMAGE_ROOT=${IMAGE_ROOT} \
  --build-arg PACKAGES_PATH=${PACKAGES_DST_REL}

remove_tmp_dir

docker run -v ${TEX_ROOT}:${IMAGE_TEX_ROOT} tinylatex \
  python3 cli.py build ${BUILD_ARGS}
