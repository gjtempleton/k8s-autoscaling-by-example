#!/usr/bin/env python
import os
import pika
import time

RABBIT_CONNECTION=os.getenv('RABBIT_CONNECTION')
RABBIT_USERNAME=os.getenv('RABBIT_USERNAME')
RABBIT_PASSWORD=os.getenv('RABBIT_PASSWORD')
MESSAGES_PER_SECOND=int(os.getenv('MESSAGES_PER_SECOND', '1'))
MESSAGE_QUEUE=os.getenv('RABBIT_MESSAGE_QUEUE', 'foo')

credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)
connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_CONNECTION, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue=MESSAGE_QUEUE)

while True:
    channel.basic_publish(exchange='',
                        routing_key=MESSAGE_QUEUE,
                        body='Bar!')
    print(f"Sent message to queue {MESSAGE_QUEUE}")
    time.sleep(1/MESSAGES_PER_SECOND)

connection.close()