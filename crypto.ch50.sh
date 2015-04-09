#!/bin/sh
cd data || exit 1
openssl rsa -in ch50.rsa -pubout -out ch50.pub > /dev/null 2>&1 || exit 1
grep -v '^-' ch50.pub | tr -d '\n'; echo
rm -f ch50.pub
cd ..
