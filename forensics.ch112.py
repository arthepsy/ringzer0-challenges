#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64

PACKETS_FILE = './data/ch112.packets.txt'

def ch112(fp):
	hline, prev = '', None
	with open(fp, 'r') as f:
		for line in f:
			if not 'Name:' in line: continue
			hx = line.strip().split(' ')[1].split('.')[0]
			if hx == prev: continue
			prev = hx
			hline += hx
	b = hline.decode('hex')
	b = base64.b64decode(b)
	print(b)

if __name__ == '__main__':
	ch112(PACKETS_FILE)

