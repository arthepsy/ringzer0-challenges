#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

BB_VOWELS = 'aeiouy'
BB_CONSONANTS = 'bcdfghklmnprstvzx'

def bb_encode(s):
	buf, c, l = 'x', 1, len(s)
	for i in range(0, l + 2, 2):
		if i >= l:
			buf += '%s%s%s' % (BB_VOWELS[c % 6],
			                   BB_CONSONANTS[16],
			                   BB_VOWELS[c / 6])
			break
		b1 = ord(s[i])
		buf += '%s%s%s' % (BB_VOWELS[(((b1 >> 6) & 3) + c) % 6],
		                   BB_CONSONANTS[(b1 >> 2) & 15],
		                   BB_VOWELS[((b1 & 3) + (c / 6)) % 6])
		if i + 1 >= l:
			break
		b2 = ord(s[i + 1])
		buf += '%s%s%s' % (BB_CONSONANTS[(b2 >> 4) & 15],
		                   '-',
		                   BB_CONSONANTS[b2 & 15])
		c = (c * 5 + b1 * 7 + b2) % 36
	buf += 'x'
	return buf

def bb_decode_sub(a1, a2, a3, offset, c):
	h = (a1 - (c % 6) + 6) % 6
	if h >= 4:
		return None, offset
	if a2 > 16:
		return None, offset + 1
	m = a2
	l = (a3 - (c/6) % 6 + 6) % 6
	if l >= 4:
		return None, offset + 2
	return h << 6 | m << 2 | l, offset

def bb_decode(s, exception = False):
	buf, c, l = '', 1, len(s)
	if l != 5 and l % 6 != 5:
		if exception: raise Exception('wrong bb "%s" length' % s)
		return None
	if s[0] != 'x':
		if exception: raise Exception('wrong bb "%s": must begin with "x"' % s)
		return None
	if s[-1:] != 'x':
		if exception: raise Exception('wrong bb "%s": must end with "x"' % s)
		return None
	ts = filter(None, re.split('(.{1,%d})' % 6, s[1:-1]))
	lt = len(ts) - 1
	for i in range(lt + 1):
		t = ts[i]
		p = i * 6
		tn = [BB_VOWELS.find(t[0]), BB_CONSONANTS.find(t[1]), BB_VOWELS.find(t[2])]
		if len(t) > 3:
			tn.append(BB_CONSONANTS.find(t[3]))
			tn.append('-')
			tn.append(BB_CONSONANTS.find(t[5]))
		t = tn
		if i == lt:
			if t[1] == 16:
				if t[0] != c % 6:
					if exception: raise Exception('wrong bb "%s" at position %d (checksum: %d)' % (s, p, c))
					return None
				if t[2] != int(c / 6):
					if exception: raise Exception('wrong bb "%s" at position %d (checksum: %d)' % (s, p + 2, c))
					return None
			else:
				b, wp = bb_decode_sub(t[0], t[1], t[2], p, c)
				if b is None:
					if exception: raise Exception('wrong bb "%s" at position %d' % (s, wp))
					return None
				buf += chr(b)
		else:
			b1, wp = bb_decode_sub(t[0], t[1], t[2], p, c)
			if b1 is None:
				if exception: raise Exception('wrong bb "%s" at position %d' % (s, wp))
				return None
			if t[3] > 16:
				if exception: raise Exception('wrong bb "%s" at position %d' % (s, p))
				return None
			if t[5] > 16:
				if exception: raise Exception('wrong bb "%s" at position %d' % (s, p + 2))
				return None
			b2 = (t[3] << 4) | t[5]
			buf += '%s%s' % (chr(b1), chr(b2))
			c = (c * 5 + b1 * 7 + b2) % 36
	return buf

def bb_tests():
	assert(bb_encode('') == 'xexax')
	assert(bb_encode('1234567890') == 'xesef-disof-gytuf-katof-movif-baxux')
	assert(bb_encode('Pineapple') == 'xigak-nyryk-humil-bosek-sonax')
	assert(bb_decode('xexax', True) == '')
	assert(bb_decode('xesef-disof-gytuf-katof-movif-baxux', True) == '1234567890')
	assert(bb_decode('xigak-nyryk-humil-bosek-sonax', True) == 'Pineapple')

if __name__ == '__main__':
	bb_tests()

