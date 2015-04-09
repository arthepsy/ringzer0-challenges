#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys

PACKETS_FILE = './data/ch117.packets.txt'

def get_key(c):
	# https://msdn.microsoft.com/en-us/library/aa299374.aspx
	if c == 1: return '<esc>'
	if c < 12: return '1234567890'[c-2]
	if c < 14: return '-='[c-12]
	spec = {14: '<backspace>', 15: '<tab>'}
	if c in spec: return spec[c]
	if c < 28: return 'qwertyuiop[]'[c-16]
	spec = {28: '<enter>', 29: '<ctrl>'}
	if c in spec: return spec[c]
	if c < 42: return 'asdfghjkl;\'`'[c-30]
	if c == 42: return '<left_shift>'
	if c < 54: return '\\zxcvbnm,.//'[c-43]
	spec = {54: '<right_shift>', 55: '*', 56: '<alt>', 57: ' ', 58: '<caps_lock>'}
	if c in spec: return spec[c]
	if c < 69: return '<f' + str(c - 58) + '>'
	spec = {69:'<num_lock>', 70:'<scroll_lock>', 
	        71:'<home>', 72:'<up>', 73:'<page_up>', 74:'<gray_->', 75:'<left>', 76:'<center>', 77:'<right>', 78:'<gray_+>', 79:'<end>', 
	        80:'<down>', 81:'<page_down>', 82:'<insert>', 83:'<del>'}
	if c in spec: return spec[c]
	spec = {87: '<f11>', 88:'<f12>'}
	if c in spec: return spec[c]
	return '<' + hex(c) + '>';

# FASTPATH_INPUT_KBDFLAGS_RELEASE	0x01
# FASTPATH_INPUT_KBDFLAGS_EXTENDED  0x02
def ch117(fp):
	assert(get_key(0x06) == '5')
	assert(get_key(0x0d) == '=')
	assert(get_key(0x17) == 'i')
	assert(get_key(0x33) == ',')
	assert(get_key(0x41) == '<f7>')
	keys = []
	with open(fp, 'r') as f:
		for line in f:
			# https://msdn.microsoft.com/en-us/library/cc240592.aspx
			if not ' 44 04 ' in line:
				continue
			line = re.sub('\s+', ' ', line.strip())
			if len(line.split(' ')) > 6:
				continue
			f = int(line.split(' ')[3], 16)
			is_extended = f & 0x02 == 0x02
			is_released = f & 0x01 == 0x01
			c = int(line.split(' ')[4], 16)
			k = get_key(c)
			# print line, hex(c)[2:].zfill(2), c, k, is_released #, is_extended
			if not is_released: keys.append(k)
	print ''.join(keys)

if __name__ == '__main__':
	ch117(PACKETS_FILE)
