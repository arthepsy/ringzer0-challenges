#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64, re, zlib

PACKETS_FILE = './data/ch115.packets.txt'

def pdf_obj_header_elem(elems, ek, ev):
	ek = (ek or '').strip()
	if ev is None: ev = ''
	if type(ev) == str: 
		ev = (ev or '').strip()
	if len(ek) == 0 and len(ev) == 0: return
	if ek in elems:
		if type(elems[ek]) == int:
			ev = elems[ek] + 1
	else:
		if len(ev) == 0: 
			ev = 1
	elems[ek] = ev
	
def pdf_obj_header_parse(raw):
	elems = {}
	l, p, state, ek, ev = len(raw), 0, 0, None, None
	while p < l:
		c, add = raw[p], True
		if c == '/':
			pdf_obj_header_elem(elems, ek, ev)
			state, ek, ev, add = 0, '', None, False
		elif c == '<':
			add = False
			if p + 1 < len and raw[p] == '<':
				np, nv = pdf_obj_header_parse(raw[p+2:])
				if state == 0:
					if len((ek or '').strip()) == 0:
						if len(elems) == 0:
							return (p + 2 + np + 1, nv)
				p, ev = p + 2 + np + 1, nv
		elif c == '>':
			pdf_obj_header_elem(elems, ek, ev)
			add = False
			if p + 1 < len and raw[p] == '>':
				p += 1
				break
		if add:
			if state == 0:
				if c == ' ':
					state = 1
					ev = ''
				else:
					ek += c
			else:
				if type(ev) == dict:
					if not c.isspace():
						if '__' not in ev: ev['__'] = ''
						ev['__'] += c
				else:
					ev += c 
		p += 1
	pdf_obj_header_elem(elems, ek, ev)
	return (p, elems)


def pdf_obj_parse(raw):
	p, header = pdf_obj_header_parse(raw)
	body = raw[p:].strip()
	return (header, body)

def pdf_obj_filter_parse(header, body):
	bl = len(body)
	if 'FlateDecode' in header:
		cl = int(header['Length']) if 'Length' in header else 0
		dl = int(header['Length1']) if 'Length1' in header else 0
		if body.startswith('stream') and body.endswith('endstream'):
			body = body[6:-9].strip('\n\r')
		decompressed = zlib.decompress(body)
		return decompressed
		
	else:
		return None

def get_cmap(raw):
	cmap = {}
	for mx in re.finditer(r'beginbfchar(.*)endbfchar', raw, re.S):
		for chrmap in re.findall('<([0-9a-f]*)> <([0-9a-f]*)>', mx.group(1), re.I or re.S):
			cmap[int(chrmap[0], 16)] = int(chrmap[1], 16)
	for mx in re.finditer(r'beginbfrange(.*)endbfrange', raw, re.S):
		for rngmap in re.findall('<([0-9a-f]*)> <([0-9a-f]*)> <([0-9a-f]*)>', mx.group(1), re.I or re.S):
			a, b, base = int(rngmap[0], 16), int(rngmap[1], 16), int(rngmap[2], 16)
			step = 1 if a <= b else -1
			for c in range(int(rngmap[0], 16), int(rngmap[1], 16) + step, step):
				cmap[c] = base + c - a
	return cmap

def ch115(fp):
	# get pdf 
	raw_data = ''
	with open(fp, 'r') as f:
		for line in f:
			if line.startswith('0000 '):
				data = line.strip().split(' ')[-1:][0]
				raw_data += data
	pdf = base64.b64decode(raw_data)
	
	# get pdf objects
	objs = {}
	for mx in re.finditer(r'^([0-9]+) ([0-9]+) obj($| *|%)?', pdf, re.M):
		if mx is None: continue
		obj_start = pdf.find('<<', mx.end())
		if obj_start == -1: continue
		obj_end_pos = pdf.find('endobj', obj_start)
		if obj_end_pos == -1: continue
		obj_id, obj_gen = int(mx.group(1)), mx.group(2)
		obj_raw = pdf[obj_start:obj_end_pos].strip()
		obj_header, obj_body = pdf_obj_parse(obj_raw)
		objs[obj_id] = {'header': obj_header, 'body': obj_body}
	
	# get cmap/content
	cmap, content = {}, ''
	for obj_id, obj in objs.items():
		#print obj_id, obj['header']
		if 'Filter' in obj['header']:
			uncompressed = pdf_obj_filter_parse(obj['header'], obj['body'])
			if obj_id == 6: content = uncompressed
			if obj_id == 8: cmap = get_cmap(uncompressed)
	
	# parse content
	txt = ''
	for chex in re.findall(r'<([0-9a-f]*)> Tj', content, re.I or re.S):
		cnum = int(chex, 16)
		if cnum in cmap: cnum = cmap[cnum]
		txt += chr(cnum)
	print txt

if __name__ == '__main__':
	ch115(PACKETS_FILE)
