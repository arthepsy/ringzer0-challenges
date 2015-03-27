#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
from subprocess import check_output

def ch159():
	ch, s = 159, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, sha1 = sections['title'], sections['hash']
	
	ringzer0.output('solving')
	result = check_output(['php', 'coding.ch159.lookup.php', sha1]).strip()
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch159()
