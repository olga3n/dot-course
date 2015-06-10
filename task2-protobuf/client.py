#!/usr/bin/env python3

import socket
import sys

import interface_pb2

import argparse

parser = argparse.ArgumentParser(conflict_handler = 'resolve')

parser.add_argument('-h', '--host', default='127.0.0.1')
parser.add_argument('-p', '--port', default=2015)

args = parser.parse_args()

PORT = int(args.port)
HOST = args.host

# -------------------------------------

item = interface_pb2.Tag()

print("New tag: \n")

text = input("Enter text: ")
while not text:
	text = input("Try again. Enter text: ")
item.text = text

url = input("Enter url (blank for none): ")
if url != '':
	item.url = url

size = input("Enter font size (blank for default): ")
if size != '':
	item.font_size = int(size)

rotation = input("Enter rotation angle (blank for none): ")
if rotation != '':
	item.rotation = int(rotation)

color = input("Enter font color 000000-FFFFFF (blank for 000000): ")
if color != '':
	item.font_color = color.encode("utf-8")

# -------------------------------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	client.connect( (HOST, PORT) )

except socket.error:
	print( 'Oops: %s\n' % (socket.error), file=sys.stderr )
	sys.exit()

data_s = item.SerializeToString()
client.sendall(data_s)

print("\nSent tag: ", item.text, file=sys.stderr )

data_l = []
while True:
	buf = client.recv(1024)
	if not buf:
		break
	data_l.append(buf)

data_r = b"".join(data_l)

client.close()

items = interface_pb2.TagCloud()
items.ParseFromString( data_r )

# -----------------------------------

print("\nItems\n")

for i in items.tag:
	print( ( "%s, %s, %i, %i, %s" % \
		(i.text, i.url, i.font_size, i.rotation, i.font_color) ) )

# -----------------------------------

import wrapper_tag_cloud

FILE = "tag_cloud.html"

fout = open(FILE, 'tw+')
fout.write( wrapper_tag_cloud.wrap(items) )
fout.close()

print( ("\nCreated: %s\n" % FILE), file=sys.stderr   )
