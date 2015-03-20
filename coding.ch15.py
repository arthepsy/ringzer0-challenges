#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import ringzer0
import re, hashlib, base64, r2pipe

def ch15():
	ch, s = 15, ringzer0.login()
	sections = ringzer0.read_challenge(s, ch)
	title, msg, chksum = sections['title'], sections['elf message'], sections['checksum']
	
	ringzer0.output('solving')
	elf = msg
	while re.match(r'^[a-zA-Z0-9+/]*={0,3}$', elf):
		elf = base64.b64decode(elf)
	elf = elf[::-1]
	elf_md5 = hashlib.md5(elf).hexdigest()
	if chksum != elf_md5:
		ringzer0.error('checksum mismatch ({0} vs {1})'.format(chksum, elf_md5))
	result = ''
	with ringzer0.tmpfile() as (fd, fn):
		ringzer0.write_bin_file(fd, elf)
		
		r2 = r2pipe.open(fn)
		asm_lines = r2.cmd('aa; s sym.main; pif~&mov,rbp').splitlines()
		asm_rg = re.compile(r'^mov [^,]*\[rbp\s?-\s?([0-9a-fx]+)\],\s?([^\s]+)$')
		asm_vals, top = {}, 0
		for asm_line in asm_lines:
			rx = re.match(asm_rg, asm_line)
			if not rx: 
				continue
			pos, val = rx.group(1), rx.group(2)
			if val.startswith('r'): 
				continue
			if val.startswith('0x'): val = val[2:]
			if len(val) % 2 == 1: val = '0' + val
			pos, val = int(pos, 16), val.decode('hex')
			asm_vals[pos] = val
			top = max(top, pos)
		stack = bytearray('\0' * top)
		
		for k in sorted(asm_vals, reverse=True):
			v = asm_vals[k]
			stack[top - k:len(v)] = v[::-1]
		result = stack[:stack.index('\00')]
	ringzer0.output('solved', result)
	
	response = ringzer0.submit_challenge(s, ch, result)
	ringzer0.output('response', response)

if __name__ == '__main__':
	ch15()
