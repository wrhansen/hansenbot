import datetime
from calendar import monthrange
from dataclasses import dataclass
from typing import Optional, Tuple

BABY_MILESTONES = ("month", "week")


@dataclass
class Milestone:
    number: int
    timeframe: str

    def __str__(self):
        plural = "s" if self.number > 1 else ""
        return f"{self.number} {self.timeframe}{plural}"


class BirthdayMixin:
    birthdate: datetime.date  # base class should provide this!

    @property
    def age(self) -> int:
        """
        Returns age (in years). If less than year old, returns 0
        """
        today = datetime.date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

    def _calc_age(self, age: int, today: Optional[datetime.date] = None) -> Milestone:
        timeframe = "year"
        age = self.age

        # Less than 2 years old -- infant/toddler milestones
        if age < 2:
            if not today:
                today = datetime.date.today()
            age_months = self.monthdelta(self.birthdate, today)

            # Less than month old --New born age milestones
            if age_months == 0:
                days = (today - self.birthdate).days
                if days % 7 == 0:
                    timeframe = "week"
                    age = days // 7
                else:
                    timeframe = "day"
                    age = days
            else:
                age = age_months
                timeframe = "month"
        return Milestone(age, timeframe)

    def _get_str_age(self, age: int) -> str:
        milestone = self._calc_age(age)
        return f"{milestone} old"

    def monthdelta(self, d1: datetime.date, d2: datetime.date) -> int:
        delta = 0
        while True:
            mdays = monthrange(d1.year, d1.month)[1]
            d1 += datetime.timedelta(days=mdays)
            if d1 <= d2:
                delta += 1
            else:
                break
        return delta

    @property
    def next_bday(self) -> int:
        today = datetime.date.today()

        this_year_bday = datetime.date(
            year=today.year, month=self.birthdate.month, day=self.birthdate.day
        )

        if this_year_bday >= today:
            next_birthday = this_year_bday
        else:
            next_birthday = datetime.date(
                year=today.year + 1, month=self.birthdate.month, day=self.birthdate.day
            )

        timedelta = next_birthday - today
        return timedelta.days

    @property
    def str_age(self) -> str:
        return self._get_str_age(self.age)

    @property
    def milestone_changed(self) -> bool:
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        today_milestone = self._calc_age(self.age)
        yesterday_milestone = self._calc_age(self.age, today=yesterday)
        if (
            today_milestone != yesterday_milestone
            and today_milestone.timeframe in BABY_MILESTONES
        ):
            return True
        return False

    @property
    def milestone(self) -> Optional[str]:
        """
        Returns a string if the current day is some special milestone. The sorts
        of milestones that are supported:
        if you're under 2 years old, return a "monthly" milestone string on each
        month, except for the 12 and 24 month period. This is because people tend
        to celebrate infants in months instead of years.
        """
        milestone = self._calc_age(self.age)
        if self.age < 2 and milestone.timeframe in BABY_MILESTONES:
            return f"{milestone}"
        return None
