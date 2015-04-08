#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import re

def ch121():
	ch, s = 121, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, shellcode = sections['title'], sections['shellcode']
	
	ringzer0.output('solving')
	sc = shellcode.replace('\\x', '').decode('hex')
	hx = sc[0x54:0x54+0x0c].encode('hex')
	result = ''.join(chr(int(x,16) ^ 0xff) for x in re.findall('..', hx))
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch121()
