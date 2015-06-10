#!/usr/bin/env python3

# nc localhost 9999 -r 2 >file.out

import socket

import sys

import argparse

parser = argparse.ArgumentParser(conflict_handler = 'resolve')

parser.add_argument('-h', '--host', default='127.0.0.1')
parser.add_argument('-p', '--port', type=int, default=9999)
parser.add_argument('-b', '--buf_size', type=int, default=2048)

args = parser.parse_args()

PORT = args.port
HOST = args.host
SIZE = args.buf_size

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	client.connect( (HOST, PORT) )
except socket.error:
	print( 'Oops: %s\n' % (socket.error), file=sys.stderr )
	sys.exit()

data = bytearray()
while True:
	buf = client.recv(SIZE)
	if not buf:
		break
	data.extend(buf)

client.close()

sys.stdout.buffer.write(data)
sys.stdout.buffer.flush()
