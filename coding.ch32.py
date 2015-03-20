#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import re

def ch32():
	ch, s = 32, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, msg = sections['title'], sections['message']
	
	ringzer0.output('solving')
	calc = ' %s ' % msg.split('=')[0]
	mx = re.findall(' ([01]+) ', calc)
	for b in mx:
		calc = calc.replace(b, str(int(b, 2)))
	result = str(eval(calc))
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch32()
