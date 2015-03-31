#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import re, hashlib

def ch48():
	ch, s = 48, ringzer0.login()
	r = s.request('GETS', ringzer0.get_url('/challenges/{0}'.format(ch)))
	response = ringzer0.get_response(r.text)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch48()
