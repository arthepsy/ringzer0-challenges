#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0, r2pipe
import string

BIN_FILE = './data/ch111.bin'

def solve_ch111(fn):
	ringzer0.output('solving')
	r2 = r2pipe.open(fn)
	asm_lines = r2.cmd('aa; s sym.main; pif~&mov dword,rbp | grep ", 0x"').splitlines()
	#   mov dword [rbp - 0x60], 0x485e2beb
	#   mov dword [rbp - 0x5c], 0xc180c931
	# (..)
	shellcode = ''
	for asm_line in asm_lines:
		val = asm_line.split(',')[-1:][0].strip()
		if val.startswith('0x'): val = val[2:]
		val = val.zfill(8)
		shellcode += val.decode('hex')[::-1]
	dlen = 0x22 - 1
	#   0x00000006    add cl, 0x22
	#   0x00000009    xor byte [esi], 0x13
	#   0x0000000c    dec eax
	#   0x0000000d    inc esi
	#   0x0000000f    loop 9
	# (..)
	dloc = 0x2d + 5
	#   0x0000002d    e8d0ffffff   call 2
	buf = shellcode[dloc:dloc+dlen]
	xr = 0x4a
	r = ''.join(chr(ord(c) ^ xr) for c in buf).strip()
	ringzer0.output('solved', r)
	return r

def ch111(offline = False):
	if offline:
		fn = BIN_FILE
		result = solve_ch111(fn)
	else:
		ch, s = 111, ringzer0.login()
		data = ringzer0.read_challenge_file(s, ch)
		with ringzer0.tmpfile() as (fd, fn):
			ringzer0.write_bin_file(fd, data)
			result = solve_ch111(fn)

if __name__ == '__main__':
	ch111(True)
