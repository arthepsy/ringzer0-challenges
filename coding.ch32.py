#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os, sys, re, datetime
import requests, hashlib
import lxml.html

VERBOSE = True
URL = 'http://ringzer0team.com'
START_TIME = datetime.datetime.now()

def _tsout(*objs):
	prefix = '[{0}]'.format(datetime.datetime.now() - START_TIME)
	print(prefix, *objs, file=sys.stdout)

def _out(*objs):
	print(*objs, file=sys.stdout)

def get_auth():
	username, password = None, None
	if not sys.stdin.isatty():
		lines = sys.stdin.readlines()
		l = len(lines)
		if l == 1:
			p = lines[0].split(' ')
			if len(p) > 1: 
				username = p[0].strip()
				password = p[1].strip()
		elif l > 1:
			username = lines[0].strip()
			password = lines[1].strip()
	else:
		username = raw_input('username: ').strip()
		password = raw_input('password: ').strip()
	if not username or not password:
		_out('error: wrong auth input')
		sys.exit(1)
	return (username, password)

def get_msg(html):
	doc = lxml.html.document_fromstring(html)
	wrapper = doc.xpath('//div[@class="challenge-wrapper"]')[0]
	text = wrapper.text_content()
	state, title, msg = 0, [], []
	for s in text.splitlines():
		s = s.strip()
		if not s: continue
		if state == 0 and s == '----- BEGIN MESSAGE -----':
			state = 1
			continue
		elif state == 1 and s == '----- END MESSAGE -----':
			state = 2
			continue
		if state == 0:
			title.append(s)
		elif state == 1:
			msg.append(s)
	return (os.linesep.join(title), os.linesep.join(msg))

def get_response(html):
	doc = lxml.html.document_fromstring(html)
	wrapper = doc.xpath('//div[@class="challenge-wrapper"]')[0]
	xalert = wrapper.xpath('./div[contains(@class, "alert")]')[0]
	return xalert.text_content().strip()

def ch32(username, password, verbose = False):
	if verbose: 
		_tsout('logging')
	s = requests.Session()
	payload = {'username':username, 'password':password}
	r = s.post(URL + '/login', data=payload)
	
	if verbose: 
		_tsout('reading challenge')
	r = s.get(URL + '/challenges/32')
	title, msg = get_msg(r.text)
	if verbose:
		_tsout('title: ' + title)
		_tsout('message: ' + msg)
	
	if verbose:
		_tsout('solving')
	calc = ' %s ' % msg.split('=')[0]
	mx = re.findall(' ([01]+) ', calc)
	for b in mx:
		calc = calc.replace(b, str(int(b, 2)))
	result = str(eval(calc))
	if verbose:
		_tsout('solved: ' + result)
	
	if verbose:
		_tsout('submitting solution')
	r = s.get(URL + '/challenges/32/' + result)
	response = get_response(r.text)
	if verbose:
		_tsout('response: ' + response)
	else:
		_out(response)


if __name__ == '__main__':
	username, password = get_auth()
	ch32(username, password, VERBOSE)
	sys.exit(0);
