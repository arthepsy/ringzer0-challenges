#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import itertools, hashlib

if __name__ == '__main__':
	chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
	for t in itertools.product(chars, repeat=6):
		w = ''.join(t)
		print(w)
