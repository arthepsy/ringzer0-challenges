#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

def ch25():
	c = 'SYNTPrfneVfPbbyOhgAbgFrpher'
	t = 'FLAG'
	for i in xrange(0, len(t)):
		cc, tc  = c[i], t[i]
		co, to = ord(cc), ord(tc)
		print(i, cc, tc, co, to, co - to, to - co, to ^ co)
	# => rot13
	print(c.encode('rot13'))

if __name__ == '__main__':
	ch25()
