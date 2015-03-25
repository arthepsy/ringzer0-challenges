#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import hashlib, itertools

def ch57():
	ch, s = 57, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, xhash, xsalt = sections['title'], sections['hash'], sections['salt']
	
	ringzer0.output('solving')
	charset = '0123456789'
	transformation = lambda x: x + xsalt
	result = search_hash(charset, 4, 4, hashlib.sha1, xhash, transformation)
	if result is None:
		ringzer0.error('could not lookup hash ' + xhash) 
	result = result[:result.rindex(xsalt)]
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

def brute_force(charset, min_len, max_len):
	return (''.join(candidate)
		for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
		for i in range(min_len, max_len + 1)))
 
def search_hash(charset, min_len, max_len, algorithm, hash_match, transformation = None):
	for v in brute_force(charset, min_len, max_len):
		if transformation:
			v = transformation(v)
		hash_curr = algorithm(v).hexdigest().lower()
		if hash_match == hash_curr:
			return v
	return None

if __name__ == '__main__':
	ch57()
