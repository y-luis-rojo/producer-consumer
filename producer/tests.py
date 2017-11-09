from django.test import TestCase

from ProducerConsumerProject.settings import X, ALLOWANCE
from producer.models import Entry, generate_random_name


class ProducerTestCase(TestCase):

    def setUp(self):
        self.randomName = generate_random_name()
        Entry.objects.create(randomName=self.randomName)

    def test_entries_stored(self):
        """
        Test an entry generated with a random name.
        :return:
        """
        entry = Entry.objects.get(randomName=self.randomName)
        self.assertGreaterEqual(len(entry.randomName), X - ALLOWANCE)
        self.assertLessEqual(len(entry.randomName), X + ALLOWANCE)