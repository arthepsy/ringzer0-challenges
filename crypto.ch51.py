#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import base64
from Crypto.Cipher import AES

def ch51():
	cpw = 'PCXrmCkYWyRRx3bf+zqEydW9/trbFToMDx6fAvmeCDw'
	dpw = gpp_decrypt(cpw)
	print(dpw)

def gpp_decrypt(cpw):
	# http://msdn.microsoft.com/en-us/library/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be%28v=PROT.13%29#endNote2
	key = '\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b'
	if len(cpw) % 4 != 0:
		cpw += "=" * (4 - len(cpw) % 4)
	c = base64.b64decode(cpw)
	iv = '\x00' * AES.block_size
	cipher = AES.new(key, AES.MODE_CBC, iv)
	d = cipher.decrypt(c)
	d = (d[:-ord(d[len(d)-1:])]).decode('utf8')
	return d

if __name__ == '__main__':
	ch51()
