#!/bin/sh

SKEL=${1}

if [ -n "${SKEL}" ] | [ ! -d "${SKEL}" ]; then
	echo "Syntax: $(basename "${0}") <skel_dir>"
	exit
fi

for FILE in $(find ${SKEL} -type f | sed -e "s#${SKEL}/##"); do
    SRC=${SKEL}/${FILE}
    DST=${HOME}/${FILE}
    if [ ! -f "${DST}" ] || [ "$(diff ${SRC} ${DST} | wc -l)" != "0" ]; then
        DST_DIR=$(dirname "${DST}")
        if [ ! -d "${DST_DIR}" ]; then
            mkdir -p "${DST_DIR}"
        fi
    	cp -v ${SRC} ${DST}
    fi
done
