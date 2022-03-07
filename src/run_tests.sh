#!/bin/bash

IMAGE_NAME=tinylatex_tests

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

docker build ${SCRIPT_DIR} -t ${IMAGE_NAME}
docker run ${IMAGE_NAME} python -m pytest .
