#  python-bdateutil
#  ----------------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/python-bdateutil
#  License: MIT (see LICENSE file)

__version__ = '0.2-dev'


# Defaults
from datetime import time
BTSTART = time(9, 0)
BTEND = time(17, 0)
WORKDAYS = range(5)
HOLIDAYS = []


import calendar
from datetime import date as basedate
from datetime import datetime as basedatetime
from datetime import time as basetime
from datetime import timedelta, tzinfo

import bdateutil
from bdateutil.parser import parse, parserinfo
from bdateutil.relativedelta import relativedelta
from bdateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU, weekday
from bdateutil.rrule import *


def isbday(dt, holidays=None):
    if holidays is None:
        holidays = HOLIDAYS
    dt = parse(dt)
    return dt.weekday() in WORKDAYS and dt not in holidays


class date(basedate):

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], basetime):
                raise TypeError("bdateutil.date cannot be initialized with "
                                "just a time")
            args = parse(args[0]).timetuple()[:3]
        return basedate.__new__(cls, *args, **kwargs)

    @staticmethod
    def today(**kwargs):
        return basedate.today() + relativedelta(**kwargs)

    @property
    def week(self):
        return self.isocalendar()[1]

    def month_start(self):
        return date(self.year, self.month, 1)

    def month_end(self):
        return date(self.year, self.month,
                    calendar.monthrange(self.year, self.month)[1])

    def year_start(self):
        return date(self.year, 1, 1)

    def year_end(self):
        return date(self.year, 12, 31)

    def add(self, **kwargs):
        return self + relativedelta(**kwargs)

    def sub(self, **kwargs):
        return self - relativedelta(**kwargs)

    def __repr__(self):
        return 'bdateutil.' + basedate.__repr__(self)


class datetime(basedatetime):

    def __new__(cls, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], basetime):
                args = (basedatetime.combine(basedatetime.today(), args[0]), )
            args = parse(args[0]).timetuple()[:6]
        return basedatetime.__new__(cls, *args, **kwargs)

    @staticmethod
    def now(**kwargs):
        return basedatetime.now() + relativedelta(**kwargs)

    @property
    def week(self):
        return self.isocalendar()[1]

    def day_start(self):
        return datetime(self.year, self.month, self.day, 0, 0, 0, 0,
                        self.tzinfo)

    def day_end(self):
        return datetime(self.year, self.month, self.day, 23, 59, 59, 999999,
                        self.tzinfo)

    def month_start(self):
        return datetime(self.year, self.month, 1, 0, 0, 0, 0, self.tzinfo)

    def month_end(self):
        return datetime(self.year, self.month,
                        calendar.monthrange(self.year, self.month)[1],
                        23, 59, 59, 999999, self.tzinfo)

    def year_start(self):
        return datetime(self.year, 1, 1, 0, 0, 0, 0, self.tzinfo)

    def year_end(self):
        return datetime(self.year, 12, 31, 23, 59, 59, 999999, self.tzinfo)

    def add(self, **kwargs):
        return self + relativedelta(**kwargs)

    def sub(self, **kwargs):
        return self - relativedelta(**kwargs)

    def __repr__(self):
        return 'bdateutil.' + basedatetime.__repr__(self)


class time(basetime):

    def __new__(self, *args, **kwargs):
        if len(args) == 1:
            args = parse(args[0]).timetuple()[3:6]
        return basetime.__new__(self, *args, **kwargs)

    @staticmethod
    def now(**kwargs):
        ret = basedatetime.now() + relativedelta(**kwargs)
        return ret.time()

    def add(self, **kwargs):
        return self + relativedelta(**kwargs)

    def sub(self, **kwargs):
        return self - relativedelta(**kwargs)

    def __repr__(self):
        return 'bdateutil.' + basetime.__repr__(self)
