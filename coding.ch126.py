#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0

# english.dat = ~/bin/scowl/mk-list english 80 > english.dat
WORDS_FILE = './data/english.dat'

def ch126(fp):
	ringzer0.output('parsing dictionary')
	wordset, wordmap = set(), {}
	with open(fp, 'r') as f:
		for line in f:
			word = line.strip()
			wordset.add(word)
			mapped = ''.join(sorted(word))
			wordmap[mapped] = word
	ringzer0.output('done parsing dictionary')
	
	ch, s = 126, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, words = sections['title'], sections['words']
	
	ringzer0.output('solving')
	result = []
	for word in words.split(','):
		if word in wordset:
			result.append(word)
			continue
		mapped = ''.join(sorted(word))
		if mapped in wordmap:
			word = wordmap[mapped]
			result.append(word)
	result = ','.join(result)
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch126(WORDS_FILE)
