#!/usr/bin/env python

import pika
import subprocess

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mystem', required=True, help="Mystem path.")
args = parser.parse_args()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ex_query', type='topic')
channel.queue_declare(queue='task_queue', durable=True)

binding_key = "#"
channel.queue_bind(exchange='ex_query', queue='task_queue', 
	routing_key=binding_key)

print '\t[worker] listen...'

def callback(ch, method, properties, body):
	
	bash_cmd = args.mystem + '/mystem -gnid '
	p1 = subprocess.Popen(['echo', '"' + body + '"'], 
		stdout=subprocess.PIPE)
	p2 = subprocess.Popen(bash_cmd.split(), stdin=p1.stdout, 
		stdout=subprocess.PIPE)

	key = method.routing_key
	message = p2.communicate()[0]

	print "\n\t[worker] %r - task:\n%s" % (method.routing_key, body)

	conn = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
	chan = conn.channel()

	chan.exchange_declare(exchange='ex_reply', type='topic')
	chan.basic_publish(exchange='ex_reply', routing_key=key, body=message)

	conn.close()

	ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

try:
	channel.start_consuming()
except KeyboardInterrupt:
	connection.close()