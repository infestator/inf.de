#!/bin/sh

if [ -z "${DEBB_HOME}" ]; then
    DEBB_HOME=$(dirname $(dirname $0))
    if [ "${DEBB_HOME}" = "." ]; then
        DEBB_HOME=$(dirname $(pwd))
    fi
fi

PYTHON_VERSION=$(python --version 2>&1 | sed -re 's/^Python ([0-9]+\.[0-9]+)\.[0-9]+$/\1/')

export DEBB_HOME
DEBB_PYTHONPATH=${DEBB_HOME}/share/debb/python
export PYTHONPATH=${DEBB_PYTHONPATH}:${PYTHON_PATH}
export PATH=${DEBB_HOME}/bin:${PATH}
