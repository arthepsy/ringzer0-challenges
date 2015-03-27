#!/bin/sh
_d=./crackstation-hashdb
_f=l6
echo "creating wordlist"
#python coding.ch159.gen_list.py > "${_f}.dat"
echo "creating indexes"
php "${_d}/createidx.php" sha1 "${_f}.dat" "${_f}-idx.dat"
echo "sorting indexes"
"${_d}/sortidx" -r 1024 "${_f}-idx.dat"
