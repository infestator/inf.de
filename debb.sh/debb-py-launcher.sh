#!/bin/bash

if [ -z "${DEBB_HOME}" ]; then
    DEBB_HOME=$(dirname $(dirname $0))
    if [ "${DEBB_HOME}" == "." ]; then
        DEBB_HOME=$(dirname $(pwd))
    fi
fi

PYTHON_VERSION=$(python --version 2>&1 | sed -re 's/^Python ([0-9]+\.[0-9]+)\.[0-9]+$/\1/')

export DEBB_HOME
DEBB_PYTHONPATH=${DEBB_HOME}/share/debb/python
export PYTHONPATH=${DEBB_PYTHONPATH}:${PYTHON_PATH}

IFS='-' read -a BASENAME <<< "$(basename "$0")"

NAME="${BASENAME[1]}"
TYPE="${BASENAME[2]}"

if [ -z "${TYPE}" ]; then
    MODULE="debb.${BASENAME[1]}"
else
    MODULE="debb.${BASENAME[2]}.${BASENAME[1]}"
fi

mkdir -p ${DEBB_HOME}/log

python -m ${MODULE} $* 2> "${DEBB_HOME}/log/${MODULE_NAME}.err" 1> "${DEBB_HOME}/log/${MODULE_NAME}.log"
