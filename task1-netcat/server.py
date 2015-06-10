#!/usr/bin/env python3

# nc -l -p 9999 <file

import sys
import socket, threading

import argparse

class thrServer(threading.Thread):
	
	def __init__(self, port, host='localhost'):
		
		threading.Thread.__init__(self)
		
		self.port = port
		self.host = host

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
		try:
			self.server.bind((self.host, self.port))
		
		except socket.error:
			print('Oops. %s' % (socket.error))
			sys.exit()

		self.server.listen(5)
		
	def run_thread(self, conn, addr, handle):
		print('Accepted client: ', addr)

		handle(conn, addr);

		conn.close()
		print( 'Closed: ', addr )

	def run(self, handle):
		print('Listening on port: %s.' % (self.port))

		while True:
			try:
				conn, addr = self.server.accept()
				threading.Thread( target=self.run_thread, 
					args=(conn, addr, handle) ).start()
			
			except KeyboardInterrupt:
				self.server.close()
				print('\nConnection closed.')
				sys.exit()

def handle(conn, addr):
	chunk = 0
	
	while chunk < len(data):
		limit = chunk + SIZE if chunk+SIZE < len(data) else len(data)

		try:
			conn.send( data[ chunk: limit ] )
		except Exception:
			raise e

		print('\t Sent bytes: %i:%i to %s' % (chunk, limit, str(addr)), 
			file=sys.stderr)

		chunk = limit
    
if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-p', '--port', type=int, default=9999)
	parser.add_argument('-b', '--buf_size', type=int, default=1024)
	parser.add_argument('-f', '--file', type=argparse.FileType('rb'))

	args = parser.parse_args()

	PORT = args.port
	SIZE = args.buf_size

	if args.file:
		FILE = args.file
	else:
		print('Read from STDIN', file=sys.stderr)
		FILE = sys.stdin.buffer

	data = FILE.read()

	server = thrServer(PORT)
	server.run(handle)
