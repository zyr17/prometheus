#!/bin/bash

date

TARGET=/var/log/prom_textfile

curdir=$(readlink -f  "$(dirname "$0")")

cd $curdir/scripts

if [[ ! -e $TARGET ]]; then
    mkdir -p $TARGET
fi

for i in *; do
    # if [[ $i != run.sh ]]; then
        echo $i
        $curdir/scripts/$i > $TARGET/$i.prom.tmp
        mv $TARGET/$i.prom.tmp $TARGET/$i.prom
    # fi
done
