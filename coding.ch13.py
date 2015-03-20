#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import re, hashlib

def ch13():
	ch, s = 13, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, msg = sections['title'], sections['message']
	
	ringzer0.output('solving')
	mx = re.search(r'using ([a-z0-9]+) algorithm', title)
	algorithm = mx.group(1)
	h = hashlib.new(algorithm)
	h.update(msg)
	result = h.hexdigest()
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch13()
