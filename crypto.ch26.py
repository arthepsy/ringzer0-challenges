#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import base64

def ch26():
	c = 'RU9CRC43aWdxNDsxaWtiNTFpYk9PMDs6NDFS'
	d = base64.b64decode(c)
	f = ''.join(chr(ord(i) ^ 3 ) for i in d)
	print(f)

if __name__ == '__main__':
	ch26()
