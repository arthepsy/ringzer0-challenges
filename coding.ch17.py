#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ringzer0
import base64
from PIL import Image
from subprocess import check_output

def solve_ch17(fn):
	black, white = (0, 0, 0), (255, 255, 255)
	bg, fg = white, black
	# open image
	img = Image.open(fn)
	mx, my = img.size
	pix = img.load()
	# remove background
	for x in range(mx):
		for y in range(my):
			if pix[x,y] == white:
				pix[x,y] = fg
			else:
				pix[x,y] = bg
	# split text
	lx, ly = 70, 23
	for c in range(6):
		for xi in range(9):
			for yi in range(12):
				x, y = lx + c*9 + xi, ly + yi
				if pix[x, y] == fg:
					nx = 15 + c*20 + xi
					pix[x, y], pix[nx, y] = bg, fg
	# scale up
	r = 3
	img = img.resize((int(round(mx * r, 2)), int(round(my * r, 2))), Image.BICUBIC) # NEAREST, BILINEAR, BICUBIC
	img.save(fn + '.ppm')
	result = check_output(['ocrad', fn + '.ppm']).strip().replace(' ', '')
	return result

def ch17():
	ch, s = 17, ringzer0.login()
	r = ringzer0.open_challenge(s, ch)
	wrapper = ringzer0.get_wrapper(r.text)
	img = wrapper.xpath('.//img')[0]
	src = img.attrib['src'].replace('data:image/png;base64,', '')
	data = base64.b64decode(src)
	with ringzer0.tmpfile() as (fd, fn):
		ringzer0.write_bin_file(fd, data)
		ringzer0.output('solving')
		result = solve_ch17(fn)
		ringzer0.output('solved', result)
		
		response = ringzer0.submit_challenge(s, ch, result)
		ringzer0.output('response', response)

if __name__ == '__main__':
	ch17()
