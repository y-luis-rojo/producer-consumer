import random
import string
import uuid

from django.db import models

NAME_MAX_LENGTH = 10
PENDING = 'pending'
COMPLETED = 'completed'


def generate_random_name(length=NAME_MAX_LENGTH, chars=string.ascii_letters + string.digits):
    """
    Generates a random name.
    :param length: Maximum length of the name
    :param chars: Chars included
    :return: Random name of type string
    """
    return ''.join(random.choice(chars) for _ in range(length))


class Entry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    randomName = models.CharField(max_length=NAME_MAX_LENGTH, default=generate_random_name)

    STATUS_CHOICES = (
        (PENDING, PENDING),
        (COMPLETED, COMPLETED)
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ''.join(['Id: ', str(self.id), ' Name: ', self.randomName, ' Status: ', self.status])