#!/usr/bin/env python

import zmq

import sys
import socket, select
import random

context = zmq.Context()

zmqsocket = context.socket(zmq.PUSH)
zmqsocket.bind("tcp://*:5557")

zmqreceiver = context.socket(zmq.PULL)
zmqreceiver.bind("tcp://*:5558")

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8080))

serversocket.listen(1)
serversocket.setblocking(0)

serversocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

connections = {}
requests = {}
responses = {}

response = b'HTTP/1.0 200 OK\n'
response += b'Content-Type: text/plain\n\n'

counter = 0

try:
	while True:
		events = epoll.poll(1)

		for fileno, event in events:
			if fileno == serversocket.fileno():
			
				connection, address = serversocket.accept()
				connection.setblocking(0)
				
				epoll.register(connection.fileno(), select.EPOLLIN)

				connections[connection.fileno()] = connection
				requests[connection.fileno()] = b''
				responses[connection.fileno()] = b''
			
			elif event & select.EPOLLIN:
				
				requests[fileno] += connections[fileno].recv(1024)
				
				if b'\n\n' in requests[fileno] or '\n\r\n' in requests[fileno]:

					print "\nclient: " + str(fileno)
					print requests[fileno].decode()

					info = str(random.randint(1, 6))

					print "client: %s; random-msg: %s" % ( str(fileno), info )

					zmqsocket.send_string(str(fileno) + ' ' + info)

					counter += 1

					epoll.modify(fileno, select.EPOLLOUT)
			
			elif responses[fileno] != b'' and (event & select.EPOLLOUT):
				
				chunk = connections[fileno].send(responses[fileno])
				responses[fileno] = responses[fileno][chunk:]
				
				if len(responses[fileno]) == 0:

					print "response to " + str(fileno)

					epoll.modify(fileno, 0)
					connections[fileno].shutdown(socket.SHUT_RDWR)
			
			elif event & select.EPOLLHUP:
				
				epoll.unregister(fileno)
				connections[fileno].close()
				
				del connections[fileno]
				del requests[fileno]
				del responses[fileno]

		if (counter > 0):
			s = zmqreceiver.recv().split()
			responses[int(s[0])] = s[1]

			counter -= 1
			
			print "worker: " + s[1].decode()

except KeyboardInterrupt:
	
	epoll.unregister(serversocket.fileno())
	epoll.close()

	serversocket.close()