from datetime import date

from django.test import TestCase
from freezegun import freeze_time
from groupme.models import Birthday


class BirthdayTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bday1 = Birthday.objects.create(
            name="Wesley Hansen", birthdate=date(2020, 8, 1)
        )
        cls.bday2 = Birthday.objects.create(
            name="Wesley Hansen", birthdate=date(2019, 8, 1)
        )
        cls.bday3 = Birthday.objects.create(
            name="Wesley Hansen", birthdate=date(1985, 5, 7)
        )
        cls.bday4 = Birthday.objects.create(
            name="Wesley Hansen", birthdate=date(2018, 8, 1)
        )

    @freeze_time("2020-12-17")
    def test_month_milestones(self):
        self.assertEqual(self.bday1.str_age, "4 months old")
        self.assertEqual(self.bday2.str_age, "16 months old")
        self.assertEqual(self.bday3.str_age, "35 years old")
        self.assertEqual(self.bday4.str_age, "2 years old")
