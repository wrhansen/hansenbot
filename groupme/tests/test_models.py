import datetime
from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from groupme.bots import BirthdayCommandBot
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

        # Infant birthdays
        cls.infant1 = Birthday.objects.create(
            name="Wesley Hansen1", birthdate=date(2021, 3, 17)
        )
        cls.infant2 = Birthday.objects.create(
            name="Wesley Hansen2", birthdate=date(2021, 3, 27)
        )
        cls.infant3 = Birthday.objects.create(
            name="Wesley Hansen3", birthdate=date(2021, 3, 28)
        )
        cls.infant4 = Birthday.objects.create(
            name="Wesley Hansen4", birthdate=date(2021, 4, 3)
        )

    @freeze_time("2020-12-17")
    def test_month_milestones(self):
        self.assertEqual(self.bday1.str_age, "4 months old")
        self.assertEqual(self.bday2.str_age, "16 months old")
        self.assertEqual(self.bday3.str_age, "35 years old")
        self.assertEqual(self.bday4.str_age, "2 years old")

    @freeze_time("2021-04-17")
    def test_infant_milestones(self):
        self.assertEqual(self.infant1.str_age, "1 month old")
        self.assertEqual(self.infant1.milestone_changed, True)
        self.assertEqual(self.infant1.milestone, "1 month")

        self.assertEqual(self.infant2.str_age, "3 weeks old")
        self.assertEqual(self.infant2.milestone, "3 weeks")
        self.assertEqual(self.infant2.milestone_changed, True)
        self.assertNotEqual(
            self.infant2._calc_age(0),
            self.infant2._calc_age(
                0, today=datetime.date.today() - datetime.timedelta(days=1)
            ),
        )

        self.assertEqual(self.infant3.str_age, "20 days old")
        self.assertEqual(self.infant3.milestone_changed, False)
        self.assertEqual(self.infant3.milestone, None)

        self.assertEqual(self.infant4.str_age, "2 weeks old")
        self.assertEqual(self.infant4.milestone_changed, True)
        self.assertEqual(self.infant4.milestone, "2 weeks")

    def test_infant_digest_message(self):

        with freeze_time("2021-04-17"):
            bot = BirthdayCommandBot()
            message = bot.digest()
            self.assertEqual(
                message,
                """Birthdays:
* New Milestone! Wesley Hansen1 is 1 month old today!
* New Milestone! Wesley Hansen2 is 3 weeks old today!
* New Milestone! Wesley Hansen4 is 2 weeks old today!""",
            )

        with freeze_time("2021-04-18"):
            bot = BirthdayCommandBot()
            message = bot.digest()
            self.assertEqual(
                message,
                """Birthdays:
* New Milestone! Wesley Hansen3 is 3 weeks old today!""",
            )

        with freeze_time("2021-05-07"):
            bot = BirthdayCommandBot()
            message = bot.digest()
            self.assertEqual(
                message,
                """Birthdays:
* Happy Birthday! Wesley Hansen turns 36 today!""",
            )
