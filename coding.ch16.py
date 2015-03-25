#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import base64, itertools, re

def ch16():
	ch, s = 16, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, hidden_xor_key, crypted_message = sections['title'], sections['xor key'], sections['crypted message']
	
	ringzer0.output('solving')
	xor_key_len = 10
	message = base64.b64decode(crypted_message)
	result = ''
	for i in range(0,len(hidden_xor_key) - xor_key_len + 1):
		xor_key = hidden_xor_key[i:i+xor_key_len]
		xored = xor_str(message, xor_key)
		alpha = re.match('^[\w-]+$', xored)
		if alpha:
			result = xored
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

def xor_str(s, key):
	return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, itertools.cycle(key)))

if __name__ == '__main__':
	ch16()
