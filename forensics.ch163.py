#!/usr/bin/env python
# -*- coding: utf-8 -*-

PACKETS_FILE = './data/ch163.packets.txt'

def ch163(fp):
	flag = [20 for i in range(37)]
	with open(fp, 'r') as f:
		for line in f:
			if not 'User id:1' in line or not 'flag AS' in line:
				continue
			p = line.strip().split(' ')
			found = p[-2:-1][0] == 'was'
			if not found:
				continue
			last = p[-3:][0]
			last, c = last.split('>')
			c, n = int(c), int(last.split(',')[2]) - 1
			if found and flag[n] < c:
				flag[n] = c
	print ''.join(chr(c + 1) for c in flag)

if __name__ == '__main__':
	ch163(PACKETS_FILE)
