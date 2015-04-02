#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko, socket, select
import os, sys
import sudoku # http://norvig.com/sudopy.shtml

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

class Sudoku:
	def __init__(self):
		pass
	
	def recv_data(self, data, is_last = False):
		cdata = data.strip()
		if is_last:
			print(cdata)
		if cdata.endswith('Solution:'):
			gridx = ''
			for line in cdata.splitlines():
				if not line.startswith('|'): continue
				line, reqrep = line.replace(' ',''), True
				while reqrep:
					l, line = len(line), line.replace('||','|.|')
					reqrep = l != len(line)
				line = line.replace('|','')
				gridx += line
			solved = sudoku.solve(gridx)
			solution = ','.join(solved[s] for s in sudoku.squares)
			return (SSH_CLEAR_DATA, '{0}\n'.format(solution))
		return (0, None)

def ch143():
	ek = 'RZ_CH143_PW'
	if not ek in os.environ:
		print('err: {0} environment variable not set'.format(ek))
		sys.exit(1)
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
	host, port, username, password = 'ringzer0team.com', 12643, 'sudoku', os.environ[ek]
	client.connect(host, port, username, password)
	chan = client.invoke_shell()
	ob = Sudoku()
	ssh_chat(chan, ob.recv_data)
	chan.close()
	client.close()

if __name__ == '__main__':
	ch143()
