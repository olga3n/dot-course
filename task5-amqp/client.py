#!/usr/bin/env python

import pika
import uuid
import sys
import re
import urllib2

key = str(uuid.uuid4())

# get random text
response = urllib2.urlopen(
	'http://www.perashki.ru/Piro/Random/?b=1&f=1&t=&a=&tag=&sort=')
html = response.read()

message = re.match(".*\"Text\">([^<]+).*", ' '.join(html.split())).group(1)

# subscription channel

conn = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
chan = conn.channel()

chan.exchange_declare(exchange='ex_reply', type='topic')

result = chan.queue_declare(exclusive=True)
queue_name = result.method.queue

chan.queue_bind(exchange='ex_reply', queue=queue_name, routing_key=key)

def callback(ch, method, properties, body):
	print "\n\t[client] %r - Result:\n%s" % (method.routing_key, body,)
	conn.close()

chan.basic_consume(callback, queue=queue_name, no_ack=True)

# publish

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ex_query', type='topic')
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='ex_query', routing_key=key, body=message, 
	properties=pika.BasicProperties( delivery_mode = 2,))

print "\n\t[client] %r - Published:\n%s" % (key, message)

connection.close()

from random import randint
from time import sleep

sleep(randint(1, 10))

# subscribe

try:
	chan.start_consuming()
except Exception:
	pass
