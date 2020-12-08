#!/usr/bin/env python
import os
import pika
import sys
import time

RABBIT_CONNECTION=os.getenv('RABBIT_CONNECTION')
RABBIT_USERNAME=os.getenv('RABBIT_USERNAME')
RABBIT_PASSWORD=os.getenv('RABBIT_PASSWORD')
MESSAGES_PER_SECOND=int(os.getenv('MESSAGES_PER_SECOND', '1'))
MESSAGE_QUEUE=os.getenv('RABBIT_MESSAGE_QUEUE', 'foo')

credentials = pika.PlainCredentials(RABBIT_USERNAME, RABBIT_PASSWORD)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_CONNECTION, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=MESSAGE_QUEUE)

    def callback(ch, method, properties, body):
        print("Received %r" % body)
        time.sleep(1/MESSAGES_PER_SECOND)

    channel.basic_consume(queue=MESSAGE_QUEUE, on_message_callback=callback, auto_ack=True)

    print(f'Waiting for messages to consume from {MESSAGE_QUEUE}.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('Finishing reading')
        sys.exit(0)
