#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

PACKETS_FILE = './data/ch12.packets.txt'

def get_key(c):
	# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
	if c < 4: return ['', '<err_roll_over>', '<post_fail>', '<err_undefined>'][c]
	if c < 40: return 'abcdefghijklmnopqrztuvwxyz1234567890'[c - 4]
	spec = {40: '<enter>', 41: '<esc>', 42: '<backspace>', 43: '<tab>'}
	if c in spec: return spec[c]
	if c < 57: return ' -=[]\\#;\'`,./'[c - 44]
	if c == 57: return '<capslock>';
	if c < 70: return '<f' + str(c - 57) + '>'
	spec = {70:'<print_screen>', 71:'<scroll_lock>', 72:'<pause>', 
	        73:'<insert>', 74: '<home>', 75: '<page_up>', 76: '<delete>', 77:'<end>', 78:'<page_down>', 
	        79:'<right>', 80:'<left>', 81:'<down>', 82:'<up>',
	        83:'<kp:numlock>', 84: '<kp:/>', 85: '<kp:*>', 86: '<kp:->', 87: '<kp:+>', 88: '<kp:enter>', 89: '<kp:1_end>', 90: '<kp:2_down>', 91: '<kp:3_page_down>', 92: '<kp:4_left>', 93: '<kp:5_>', 94: '<kp:6_right>', 95: '<kp:7_home>', 96: '<kp:8_up>', 97: '<kp:9_page_down>', 98: '<kp:0_insert>', 99: '<kp:._delete>', 103: '<kp:=>',
	        100: '\\', 101: '<application>', 102: '<power>'}
	if c in spec: return spec[c]
	return '<0x' + hex(c) + '>';

def ch12(fp):
	keys = []
	with open(fp, 'r') as f:
		for line in f:
			if not 'Capture Data:' in line:
				continue
			data = line.strip().split(' ')[-1:][0]
			c = int(data[4:6], 16)
			k = get_key(c)
			keys.append(k)
	print ''.join(keys)

if __name__ == '__main__':
	ch12(PACKETS_FILE)
