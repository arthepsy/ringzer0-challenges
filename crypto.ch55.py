#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import base64
from Crypto.Cipher import AES
from Crypto import Random

SS_DEFAULT_HEADER = '76492d1116743f0423413b16050a5345'
SS_DEFAULT_ENCODING = 'utf_16_le'

def convert_from_secure_string(key, data, header = SS_DEFAULT_HEADER, enc = SS_DEFAULT_ENCODING, iv = None):
	key_str = str(bytearray(key))
	padlen = 16 - (len(data) % 16)
	data += chr(padlen)*padlen
	if iv is None:
		iv = Random.new().read(AES.block_size)
	iv_str = str(bytearray(iv))
	cipher = AES.new(key_str, AES.MODE_CBC, iv_str)
	ciphertext = cipher.encrypt(data)
	rest_raw = '2|{0}|{1}'.format(base64.b64encode(iv_str), ciphertext.encode('hex'))
	if enc:
		rest_raw = rest_raw.encode(enc)
	rest_b64 = base64.b64encode(rest_raw)
	output = header + rest_b64
	return output

def convert_to_secure_string(key, data, header = SS_DEFAULT_HEADER, enc = SS_DEFAULT_ENCODING):
	key_str = str(bytearray(key))
	data = data[len(header):]
	p = base64.b64decode(data)
	if enc:
		p = p.decode(enc)
	p = p .split('|')
	if len(p) != 3 or p[0] != '2':
		return None
	iv_str = base64.b64decode(p[1])
	ciphertext = p[2].decode('hex')
	cipher = AES.new(key_str, AES.MODE_CBC, iv_str)
	d = cipher.decrypt(ciphertext)
	d = (d[:-ord(d[len(d)-1:])])
	return d

if __name__ == '__main__':
	key = [3,4,2,3,56,34,254,222,205,34,2,23,42,64,33,223,1,34,2,7,6,5,35,12]
	msg = '76492d1116743f0423413b16050a5345MgB8AEEAYQBNAHgAZQAxAFEAVABIAEEAcABtAE4ATgBVAFoAMwBOAFIAagBIAGcAPQA9AHwAZAAyADYAMgA2ADgAMwBlADcANAA3ADIAOQA1ADIAMwA0ADMAMwBlADIAOABmADIAZABlAGMAMQBiAGMANgBjADYANAA4ADQAZgAwADAANwA1AGUAMgBlADYAMwA4AGEAZgA1AGQAYgA5ADIAMgBkAGIAYgA5AGEAMQAyADYAOAA='
	out = convert_to_secure_string(key, msg, '76492d1116743f0423413b16050a5345')
	print(out)
