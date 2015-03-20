#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import hashlib, itertools

def ch56():
	ch, s = 56, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, xhash = sections['title'], sections['hash']
	
	ringzer0.output('solving')
	charset = '0123456789'
	result = search_hash(charset, 4, 4, hashlib.sha1, xhash)
	if result is None:
		ringzer0.error('could not lookup hash ' + xhash) 
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

def brute_force(charset, min_len, max_len):
	return (''.join(candidate)
		for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
		for i in range(min_len, max_len + 1)))
 
def search_hash(charset, min_len, max_len, algorithm, hash_match):
	for v in brute_force(charset, min_len, max_len):
		hash_curr = algorithm(v).hexdigest().lower()
		if hash_match == hash_curr:
			return v
	return None

if __name__ == '__main__':
	ch56()
