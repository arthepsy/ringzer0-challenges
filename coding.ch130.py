#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko, socket, select
import os, sys, re, math

SSH_CLEAR_DATA = 1
SSH_BREAK_CHAT = 2

def ssh_chat(chan, data_cb):
	data = ''
	while True:
		chan.settimeout(0.0)
		rl, wl, xl = select.select([chan], [], [])
		try:
			b = chan.recv(1024)
			if len(b) == 0:
				break
			data += b
			action, reply = data_cb(data)
			if action > 0 and action & SSH_CLEAR_DATA == SSH_CLEAR_DATA:
				data = ''
			if reply is not None:
				chan.sendall(reply)
			if action > 0 and action & SSH_BREAK_CHAT == SSH_BREAK_CHAT:
				break
		except socket.timeout:
			pass
	data_cb(data, True)

class NumGame:
	def __init__(self):
		self.games_won = 0
		self.reset()
	
	def reset(self):
		self.num_min = 0
		self.num_max = int(math.sqrt(math.sqrt(sys.maxint)))
		self.guess = 0
	
	def get_next_guess(self):
		self.guess = (self.num_min + self.num_max) / 2
		return self.guess
	
	def set_guess_result(self, is_smaller):
		if is_smaller:
			self.num_min = self.guess
		else:
			self.num_max = self.guess
	
	def recv_data(self, data, is_last = False):
		cdata = data.strip()
		if is_last:
			p = cdata.find('You beat')
			if p != -1:
				print(cdata[p:]) 
			else:
				print(cdata)
			return
		mx = re.search(r'Game that you win ([0-9]+)', cdata, re.S)
		if mx is not None:
			self.games_won = int(mx.group(1))
		if 'You got the right number' in cdata:
			print('guessed correct: {0}'.format(self.guess))
			print('games won: {0}'.format(self.games_won))
			self.reset()
		else:
			mx = re.search(r'Your number is too (big|small)\.', cdata, re.S)
			if mx is not None:
				is_smaller = mx.group(1) == 'small'
				print('guessed wrong: {0} too {1}'.format(self.guess, mx.group(1)))
				self.set_guess_result(is_smaller)
		if cdata.endswith('number>'):
			#print "#NUMBER", data
			return (SSH_CLEAR_DATA, '{0}\n'.format(self.get_next_guess()))
			#return (SSH_BREAK_CHAT, None)
		return (0, None)

def ch130():
	ek = 'RZ_CH130_PW'
	if not ek in os.environ:
		print('err: {0} environment variable not set'.format(ek))
		sys.exit(1)
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
	host, port, username, password = 'ringzer0team.com', 12643, 'number', os.environ[ek]
	client.connect(host, port, username, password)
	chan = client.invoke_shell()
	ng = NumGame()
	ssh_chat(chan, ng.recv_data)
	chan.close()
	client.close()

if __name__ == '__main__':
	ch130()
