#!/usr/bin/env python
from multiprocessing.connection import Listener
from multiprocessing.connection import Client
from multiprocessing import AuthenticationError
import threading
import time
import sys
import os

class MiniChat(object):
	def __init__(self, host_and_port, nickname, auth_key):
		self.chat_log = []
		self.host, self.port = host_and_port.split(':')
		self.port = int(self.port)
		self.nickname = nickname
		self.auth_key = auth_key
		self.running = True
		self.connection = None
		self.listener = None
		os.system('cls' if os.name == 'nt' else 'clear')

	def stop(self):
		self.running = False
		if self.connection:
			self.connection.close()

	def add_message(self, message):
		self.chat_log.append(message)
		os.system('cls' if os.name == 'nt' else 'clear')
		print '\n'.join(self.chat_log)

	def run_host(self):
		self._run_threaded(self._run_host_forever)

	def run_client(self):
		self._run_threaded(self._run_client_forever)

	def _run_threaded(self, target):
		thread = threading.Thread(target=target)
		thread.daemon = True
		thread.start()
		self.handle_inputs()

	def _run_host_forever(self):
		self.add_message('Chat server running on port %d' % self.port)
		self.listener = Listener((self.host, self.port), authkey=self.auth_key)
		while self.running:
			try:
				self.connection = self.listener.accept()
				self.add_message('Client has connected.')
				self.handle_messages()
			except (IOError, EOFError):
				if self.running:
					self.add_message('Client has disconnected.')
			except AuthenticationError:
				self.add_message('Client tried to connect with wrong password.')
		self.listener.close()

	def _run_client_forever(self):
		self.add_message('Connecting to chat server %s on port %d' % (self.host, self.port))
		while self.running:
			try:
				self.connection = Client((self.host, self.port), authkey=self.auth_key)
				self.add_message('Connected to host.')
				self.handle_messages()
			except (IOError, EOFError):
				if self.running:
					self.add_message('Host has disconnected.')
			except AuthenticationError:
				self.add_message('Wrong password.')
				self.stop()

	def handle_messages(self):
		while self.running:
			self.add_message(self.connection.recv())
		self.connection.close()

	def handle_inputs(self):
		while self.running:
			while self.running and not self.connection:
				time.sleep(0.2)
			if self.connection:
				text = self.nickname + ': ' + raw_input()
				self.add_message(text)
				self.connection.send(text)

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print 'usage server: python minichat.py -host host:port nickname password \nusage client: python minichat.py -connect host:port nickname password\nCTRL+C to exit.'
	else:
		try:
			chat = MiniChat(host_and_port=sys.argv[2], nickname=sys.argv[3], auth_key=sys.argv[4])
			if sys.argv[1] == '-host':
				chat.run_host()
			elif sys.argv[1] == '-connect':
				chat.run_client()
		except KeyboardInterrupt:
			chat.stop()
			print 'Chat ended.'
		except ValueError as e:
			print 'Invalid argument: ' + str(e)
