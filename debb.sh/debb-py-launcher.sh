#!/bin/sh

if [ -z "${DEBB_HOME}" ]; then
	DEBB_HOME=$(dirname $(dirname $0))
fi

PYTHON_VERSION=$(python --version 2>&1 | sed -re 's/^Python ([0-9]+\.[0-9]+)\.[0-9]+$/\1/')

export PYTHON_DEBB_OATH=${DEBB_HOME}/share/debb/python
export PYTHON_PATH=${PYTHON_DEBB_PATH}:${PYTHON_PATH}

python ${PYTHON_DEBB_PATH}/${SCRIPT}