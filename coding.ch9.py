#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0, r2pipe

def solve_ch9(fn):
	ringzer0.output('solving')
	# idx=05 vaddr=0x00406000 paddr=0x00001e00 sz=7680 vsz=7256 perm=-rw- name=.rsrc
	exe_rsrc_vaddr = 0x00406000
	exe_rsrc_paddr = 0x00001e00
	exe_dll_vaddr =  0x00406058
	exe_dll_paddr = exe_rsrc_paddr + (exe_dll_vaddr - exe_rsrc_vaddr)
	# idx=02 vaddr=0x6e5c3000 paddr=0x00001000 sz=1024 vsz=640 perm=-r-- name=.rdata
	dll_rodata_vaddr = 0x6e5c3000
	dll_rodata_paddr = 0x1000
	# |          0x6e5c120f    be60305c6e   mov esi, 0x6e5c3060
	dll_buf_location_vaddr = 0x6e5c3060
	dll_buf_location_paddr = dll_rodata_paddr + (dll_buf_location_vaddr - dll_rodata_vaddr)
	exe_buf_location_paddr = exe_dll_paddr + dll_buf_location_paddr
	# |          0x6e5c1244    83fe1f       cmp esi, 0x1f
	buf_size = 0x1f
	cmd = 'pf {%d}i @ %d' % (buf_size, exe_buf_location_paddr)
	
	buf_data = ''
	r2 = r2pipe.open(fn)
	for line in r2.cmd(cmd).splitlines():
		# .->    0x6e5c121c    8b04b2       mov eax, dword [edx + esi*4]
		# |      0x6e5c121f    83e816       sub eax, 0x16
		hx = int(line.split(' ')[-1:][0])
		hx = hx - 0x16
		buf_data += chr(hx)
	ringzer0.output('solved', buf_data)
	return buf_data

def ch9(offline = False):
	if offline:
		fn = 'ch9.exe'
		result = solve_ch9(fn)
	else:
		ch, s = 9, ringzer0.login()
		data = ringzer0.read_challenge_file(s, ch)
		with ringzer0.tmpfile() as (fd, fn):
			ringzer0.write_bin_file(fd, data)
			result = solve_ch9(fn)

if __name__ == '__main__':
	ch9(False)
