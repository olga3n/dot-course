#!/usr/bin/env python

import zmq
import sys
import time

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

while True:
	try:
		msg = receiver.recv().split()
		
		if msg:			
			
			# smth work
			time.sleep(int(msg[1]) * 0.2)

			# smth result
			text = b'ok' + b'a' * int(msg[1]) + b'y.'

			sender.send( msg[0] + ' ' + text )

			print "client: %s; recv: %s; send: %s" % ( 
				msg[0], msg[1], str(text) )

	except KeyboardInterrupt:
		sys.exit()