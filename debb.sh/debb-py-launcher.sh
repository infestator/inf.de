#!/bin/bash

. $(dirname $0)/debb-env.sh

IFS='-' read -a BASENAME <<< "$(basename "$0")"

NAME="${BASENAME[1]}"
TYPE="${BASENAME[2]}"

if [ -z "${TYPE}" ]; then
    MODULE="debb.${BASENAME[1]}"
else
    MODULE="debb.${BASENAME[2]}.${BASENAME[1]}"
fi

mkdir -p ${DEBB_HOME}/log

echo "Running ${MODULE}"

echo ${PYTHONPATH}

python -m ${MODULE} $*