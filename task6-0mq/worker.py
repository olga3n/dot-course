#!/usr/bin/env python

import zmq
import sys
import os, posixpath, mimetypes, cgi

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

while True:
	try:
		msg = receiver.recv().split()
		
		if msg:			
			
			result = b''
			header = b'HTTP/1.0 404\n'

			if len(msg) > 1:
				path = msg[1]
			else:
				path = '.'

			if os.path.isdir(path):
				try:
					list = os.listdir(path)
					list.sort(lambda a, b: cmp(a.lower(), b.lower()))
					
					result = "<title>Directory listing for %s</title>\n" % path
					result += "<h2>Directory listing for %s</h2>\n" % path
					result += "<hr>\n<ul>\n"
					for name in list:
						fullname = os.path.join(path, name)
						displayname = linkname = name = cgi.escape(name)
						if os.path.isdir(fullname):
							displayname = name + "/"
							linkname = name + "/"
						if os.path.islink(fullname):
							displayname = name + "@"
						result += '<li><a href="%s">%s</a></li>\n' % (linkname, displayname)
					result += "</ul>\n<hr>\n"
					
					header = b'HTTP/1.0 200 OK\n'
					header += b'Content-Type: text/html\n\n'
				except os.error:
					pass
			else:
				base, ext = posixpath.splitext(path)
				extensions_map = mimetypes.types_map.copy()
				if extensions_map.has_key(ext):
					ctype = extensions_map[ext]
				else:
					ctype = 'application/octet-stream'

				header = b'HTTP/1.0 200 OK\n'
				header += b'Content-Type: ' + ctype + b'\n\n'

				mode = 'rb'
				try:
					f = open(path, mode)
					result += f.read()
					f.close()

				except Exception:
					pass

			print "client: %s; recv: /%s" % ( msg[0], path )

			sender.send( msg[0] + '\n' + header + result )

	except KeyboardInterrupt:
		sys.exit()