#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0

ascii_digits = '''\
 xxx  |x   x |x   x |x   x | xxx  |0|
 xx   |x x   |  x   |  x   |xxxxx |1|
 xxx  |x   x |  xx  | x    |xxxxx |2|
 xxx  |x   x |  xx  |x   x | xxx  |3|
 x   x|x    x| xxxxx|     x|    x |4|
xxxxx |x     | xxxx |    x |xxxxx |5|
'''.splitlines()
ascii_table = {}
for form in ascii_digits:
	if not '|' in form: continue
	ascii_table[form[-2]] = form[:-3].split('|')
ascii_rows = len(ascii_table.values()[0])


def parse_ascii(data):
	numbers = []
	n, dln = 0, 0
	for line in data.splitlines():
		if 'x' not in line: continue
		line = line.ljust(6, ' ')
		if dln == 0: numbers.append([])
		numbers[n].append(line)
		if dln == 4:
			dln = 0
			n += 1
		else:
			dln += 1
	numline = ''
	for number in numbers:
		for k, v in ascii_table.items():
			if v == number:
				numline += k
	return numline

def ch119():
	ch, s = 119, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch, clean=False)
	title, msg = sections['title'], sections['message']
	
	ringzer0.output('solving')
	result = parse_ascii(msg)
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch119()
