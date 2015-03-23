#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0, r2pipe

def solve_ch11(fn):
	ringzer0.output('solving')
	r2 = r2pipe.open(fn)
	asm_lines = r2.cmd('aa; s sym.main; pif~&mov,word,eax | grep ", 0x"').splitlines()
	#   mov dword [eax], 0x47414c46
	#   mov dword [eax + 4], 0x3930342d
	#   mov word [eax + 8], 0x32
	#   mov dword [eax], 0x75393438
	#   mov dword [eax + 4], 0x6a326f69
	#   mov word [eax + 8], 0x66
	#   mov dword [eax], 0x6a736c6b
	#   mov dword [eax + 4], 0x6c6b34
	buf = ''
	for asm_line in asm_lines:
		val = asm_line.split(',')[-1:][0].strip()
		if val.startswith('0x'): val = val[2:]
		buf += val.decode('hex')[::-1]
	ringzer0.output('solved', buf)
	return buf

def ch11(offline = False):
	if offline:
		fn = 'ch11.bin'
		result = solve_ch11(fn)
	else:
		ch, s = 11, ringzer0.login()
		data = ringzer0.read_challenge_file(s, ch)
		with ringzer0.tmpfile() as (fd, fn):
			ringzer0.write_bin_file(fd, data)
			result = solve_ch11(fn)

if __name__ == '__main__':
	ch11(False)
