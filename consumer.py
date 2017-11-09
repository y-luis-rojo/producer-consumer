#!/usr/bin/env python
import logging

import pika

import os

import django

from ProducerConsumerProject.settings import RABBITMQ_HOST, NOTIFICATION_MESSAGE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProducerConsumerProject.settings")
django.setup()

from producer.models import Entry, COMPLETED, PENDING

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)


class Consumer:
    """
    Consumer class which uses pika package
    """
    def __init__(self, host):
        self.queue = 'entries'
        self.connect(host)
        self.channel.basic_consume(self.callback, queue=self.queue, no_ack=True)

    def __del__(self):
        logging.info('Closing connection...')
        self.connection.close()

    def connect(self, host):
        """
        Connect to a RabbitMQ service.
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    @staticmethod
    def callback(ch, method, properties, body):
        """
        Callback to be executed when a notification arrives
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        if body == NOTIFICATION_MESSAGE:
            entries = Entry.objects.filter(status=PENDING)
            count = entries.count()
            entries.update(status=COMPLETED)
            logging.info('Updated {0} entries'.format(count))

    def run(self):
        """
        Start listening
        :return:
        """
        logging.info('Waiting for entries notifications...')
        self.channel.start_consuming()


Consumer(RABBITMQ_HOST).run()
