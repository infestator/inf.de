#!/bin/bash

if [ -z "${DEBB_HOME}" ]; then
	DEBB_HOME=$(dirname $(dirname $0))
	if [ "${DEBB_HOME}" == "." ]; then
		DEBB_HOME=$(dirname $(pwd))
	fi
fi

PYTHON_VERSION=$(python --version 2>&1 | sed -re 's/^Python ([0-9]+\.[0-9]+)\.[0-9]+$/\1/')

export DEBB_PYTHONPATH=${DEBB_HOME}/share/debb/python
export PYTHONPATH=${DEBB_PYTHONPATH}:${PYTHON_PATH}

IFS='-' read -a BASENAME <<< "$(basename "$0")"

NAME="${BASENAME[1]}"
TYPE="${BASENAME[2]}"

if [ -z "${TYPE}" ]; then
	SCRIPT="debb/${NAME}.py"
else
	SCRIPT="debb/${TYPE}/${NAME}.py"
fi

#echo $PYTHON_PATH

python "${DEBB_PYTHONPATH}/${SCRIPT}"