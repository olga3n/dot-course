#!/usr/bin/env python3

import sys, os
import socket, threading
import argparse

import interface_pb2

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
				break

def handle(conn, addr):

	data_r = conn.recv( 1024*16 )	

	new = interface_pb2.Tag()
	new.ParseFromString( data_r )

	print("read tag: ", new.text)

	with lock:
		items.tag.add().CopyFrom(new)

	data_s = items.SerializeToString()

	conn.sendall(data_s)

	print("sent list to: ", addr)
	
    
if __name__ == '__main__':

	parser = argparse.ArgumentParser()

	parser.add_argument('-p', '--port', default=2015)
	parser.add_argument('-f', '--file', default="tag_cloud.bin")

	args = parser.parse_args()

	PORT = int(args.port)
	FILE = args.file

	items = interface_pb2.TagCloud()

	if os.path.isfile(FILE):
		with open(FILE, 'rb+') as f:
			items.ParseFromString( f.read() )

	lock = threading.Lock()

	server = thrServer(PORT)
	server.run(handle)

	if len(items.tag) > 0:
		
		fout = open(FILE, 'wb+')
		fout.write(items.SerializeToString())
		fout.close()
