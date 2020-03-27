#!/bin/bash
# Version: 2.0
# Developer: ilan.shavit@gmail.com

error_msg() {
    echo "Usage: ts -c -s filename (copy file - short timestamp)"
    echo "       ts -c -f filename (copy file - full timestamp)"
    echo "       ts -m -s filename (move file - short timestamp)"
    echo "       ts -m -f filename (move file - full timestamp)"
}

full_ts=$(date  +%Y-%m-%d_%H-%M-%S)
short_ts=$(date  +%Y-%m-%d)
if [ $# = 3 ]; then
    if [ "$1" = -c ]; then
        if [ "$2" = -s ] ; then
            cp -p "$3" "$3_$short_ts"
        elif [ "$2" = -f ] ; then
            cp -p "$3" "$3_$full_ts"
        else
            error_msg
        fi
    elif [ "$1" = -m ] ; then
        if [ "$2" = -s ] ; then
            mv "$3" "$3_$short_ts"
        elif [ "$2" = -f ] ; then
            mv "$3" "$3_$full_ts"
        else
            error_msg
        fi
    else
        error_msg
    fi
else
        error_msg
fi
