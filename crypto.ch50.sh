#!/bin/sh
openssl rsa -in ch50.rsa -pubout -out ch50.pub > /dev/null 2>&1
grep -v '^-' ch50.pub | tr -d '\n'; echo
