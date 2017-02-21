# coding: utf-8
from datetime import datetime, timedelta


__all__ = ('Interval',)


class Interval(object):
    def __init__(self, years=None, months=None, days=None, hours=None,
                 minutes=None, weekdays=None,
                 max_search_delta=timedelta(hours=2)):
        self.years = set(years) if years else None
        self.months = None
        self.days = None
        self.hours = None
        self.minutes = None
        self.weekdays = None
        self.max_search_delta = max_search_delta

        if months:
            if not all(1 <= month <= 12 for month in months):
                raise ValueError('Invalid month')
            self.months = set(months)

        if days:
            if not all(1 <= day <= 31 for day in days):
                raise ValueError('Invalid day')
            self.days = set(days)

        if hours:
            if not all(0 <= hour <= 23 for hour in hours):
                raise ValueError('Invalid hour')
            self.hours = set(hours)

        if minutes:
            if not all(0 <= minute <= 59 for minute in minutes):
                raise ValueError('Invalid minute')
            self.minutes = set(minutes)

        if weekdays:
            if not all(1 <= weekday <= 7 for weekday in weekdays):
                raise ValueError('Invalid weekday')
            self.weekdays = set(weekdays)

    def get_next_time(self):
        cur_dt = datetime.now()
        max_dt = cur_dt + self.max_search_delta
        while cur_dt <= max_dt:
            cur_dt += timedelta(minutes=1)
            found = (
                (self.years is None or cur_dt.year in self.years) and
                (self.months is None or cur_dt.month in self.months) and
                (self.days is None or cur_dt.day in self.days) and
                (self.hours is None or cur_dt.hour in self.hours) and
                (self.minutes is None or cur_dt.minute in self.minutes) and
                (self.weekdays is None or cur_dt.isoweekday() in self.weekdays)
            )
            if found:
                return cur_dt

        return None
