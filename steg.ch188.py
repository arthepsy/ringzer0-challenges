#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0

def solve_ch188(fn):
	ringzer0.output('solving')
	flag = ''
	with open(fn, 'r') as f:
		for rline in f:
			line = rline[:-1]
			hx = line[:47].replace(' ', '')
			tx = line[51:]
			ex = hx.decode('hex').replace('\n', ' ')
			if ex != tx:
				for i in range(len(tx)):
					if tx[i] != ex[i]:
						flag += ex[i]
	ringzer0.output('solved', flag)
	return flag

def ch188(offline = False):
	if offline:
		fn = './data/steg.ch188.txt'
		result = solve_ch188(fn)
	else:
		ch, s = 188, ringzer0.login()
		data = ringzer0.read_challenge_file(s, ch)
		with ringzer0.tmpfile() as (fd, fn):
			ringzer0.write_bin_file(fd, data)
			result = solve_ch188(fn)

if __name__ == '__main__':
	ch188()
