#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib

ACCESS_LOG_FILE = 'ch164.access.log'

def ch164(fp):
	flag = [[0,0,0,0,0,0,0,0] for i in range(38)]
	b64 = []
	with open(fp, 'r') as f:
		for line in f:
			line = line.strip()
			if len(line) == 0: continue
			if 'flag' not in line: continue
			p = line.split(' ')
			req, size = p[6][18:], int(p[9])
			req = urllib.unquote(req)
			if req.startswith('admin'):
				ol = len(req)
				zero = (size - ol - 229) == 0
				p = req.split(',')
				n, b = int(p[1]), int(p[5])
				flag[n-1][8-b] = '0' if zero else '1'
	hx = [hex(int(''.join(map(str,bulk)), 2))[2:] for bulk in flag]
	print ''.join(chr(int(x, 16)) for x in hx)

if __name__ == '__main__':
	ch164(ACCESS_LOG_FILE)
