#!/bin/sh

S=${1}

if [ -n "${S}" ] | [ ! -d "${S}" ]; then
	echo "Syntax: $(basename "${S}") <skel_dir>"
	exit
fi

for F in $(ls -a ${S} | egrep -v '^\.*$'); do
	cp -ivr ${S}/${F} ${HOME}
done
