#!/bin/sh

SKEL=${1}

if [ -n "${SKEL}" ] | [ ! -d "${SKEL}" ]; then
	echo "Syntax: $(basename "${SKEL}") <skel_dir>"
	exit
fi

OLD_PWD=${PWD}
cd ${SKEL}
for FILE in $(find -type f); do
    FILE="$(expr substr "${FILE}" 3 $(($(expr length "${FILE}")-2)))"
    mkdir -p "$(dirname "${FILE}")"
    echo ${FILE}
    if [ -f ${HOME}/${FILE} ]; then
        diff "${HOME}/${FILE}" "${FILE}"
    	cp -iv "${HOME}/${FILE}" "${FILE}"
    else
        rm -iv "${FILE}"
    fi
done
cd ${OLD_PWD}
