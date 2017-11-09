#!/usr/bin/env python
import random

import pika
import logging
import threading

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ProducerConsumerProject.settings")
django.setup()

from ProducerConsumerProject.settings import ALLOWANCE, X, RABBITMQ_HOST, NOTIFICATION_MESSAGE

from producer.models import Entry

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)


class Producer:
    """
    Producer class which uses pika package
    """
    def __init__(self, host):
        self.queue = 'entries'
        self.connect(host)

    @staticmethod
    def generate_size(x=X, allowance=ALLOWANCE):
        """
        Function to generate a number between :x - :allowance and :x + :allowance
        :param x:
        :param allowance:
        :return:
        """
        delta = random.randint(0, allowance)

        if random.random() < 0.5:
            return x + delta

        return x - delta

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

    def create_new_entries(self):
        """
        Generate a list of Entry with default values.
        :return: List of Entry
        """
        entries = []

        for _ in range(0, self.generate_size()):
            entries.append(Entry())

        logging.info('Created {0} entries'.format(len(entries)))
        return entries

    @staticmethod
    def insert_entries(entries):
        """
        Bulk insert a list of Entry
        :param entries: List of Entry
        """
        Entry.objects.bulk_create(entries)
        logging.info('Saved {0} entries'.format(len(entries)))

    def run(self, period):
        """
        Start the producer. Generates entries, store them in db and notify broker.
        :param period: Period to repeat
        :return:
        """
        entries = self.create_new_entries()
        self.insert_entries(entries)

        # Send notification message
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=NOTIFICATION_MESSAGE)

        # Schedule repeat
        threading.Timer(period, self.run).start()


Producer(RABBITMQ_HOST).run(60)