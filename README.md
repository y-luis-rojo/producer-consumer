[![Build Status](https://travis-ci.org/y-luis/producer-consumer.svg?branch=master)](https://travis-ci.org/y-luis/producer-consumer)

# producer-consumer

Producer-Consumer system using RabbitMQ.

Prerequisites:
-------------
Django

pika

RabbitMQ server

Instructions
-------------
Producer and Consumer use Django ORM. A settings file with default required values is provided as example.

- Create database
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python producer.py` to run Producer
- `python consumer.py` to run Consumer


Tested with:
-------------
Django 1.10

Python 2.7.13

pika 0.11
