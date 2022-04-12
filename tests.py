#  python-bdateutil
#  ----------------
#  Adds business day logic and improved data type flexibility to
#  python-dateutil. 100% backwards compatible with python-dateutil,
#  simply replace dateutil imports with bdateutil.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/python-bdateutil
#  License: MIT (see LICENSE file)


import datetime as dt
import unittest

import holidays

from dateutil.tz import datetime_ambiguous, datetime_exists
from test_dateutil_28.test_easter import *
from test_dateutil_28.test_imports import *
from test_dateutil_28.test_parser import *
from test_dateutil_28.test_relativedelta import *
from test_dateutil_28.test_rrule import *
from test_dateutil_28.test_tz import *

import bdateutil
from bdateutil import isbday
from bdateutil import easter
from bdateutil import relativedelta
from bdateutil import parse, parserinfo
from bdateutil.rrule import *
from bdateutil import date, datetime, time


class TestIsBday(unittest.TestCase):

    def test_isbday(self):
        self.assertFalse(isbday(date(2014, 1, 4)))
        self.assertFalse(isbday("2014-01-04"))
        self.assertTrue(isbday(date(2014, 1, 1)))
        self.assertTrue(isbday("2014-01-01"))
        self.assertFalse(isbday(date(2014, 1, 1), holidays=holidays.US()))
        self.assertTrue(isbday(datetime(2014, 1, 1, 16, 30)))
        self.assertTrue(isbday(datetime(2014, 1, 1, 17, 30)))
        self.assertFalse(isbday(datetime(2014, 1, 1, 16, 30),
                         holidays=holidays.US()))
        self.assertFalse(isbday(datetime(2014, 1, 1, 17, 30),
                         holidays=holidays.US()))
        bdateutil.HOLIDAYS = holidays.Canada()
        self.assertFalse(isbday(date(2014, 7, 1)))
        self.assertTrue(isbday(date(2014, 7, 4)))
        self.assertFalse(isbday(date(2014, 1, 1)))
        self.assertTrue(isbday(date(2014, 7, 1), holidays=holidays.US()))
        self.assertFalse(isbday(date(2014, 7, 4), holidays=holidays.US()))
        bdateutil.HOLIDAYS = []


class TestRelativeDelta(unittest.TestCase):

    def test_init(self):
        self.assertEqual(relativedelta(date(2014, 1, 7), date(2014, 1, 3)),
                         relativedelta(days=4, bdays=2))
        self.assertEqual(relativedelta(date(2014, 1, 31), date(2014, 1, 1)),
                         relativedelta(days=30, bdays=22))
        self.assertEqual(relativedelta(date(2014, 2, 1), date(2014, 1, 1)),
                         relativedelta(months=1, bdays=22))
        self.assertEqual(relativedelta(date(2014, 2, 2), date(2014, 1, 1)),
                         relativedelta(months=1, days=1, bdays=22))
        self.assertEqual(relativedelta(date(2014, 1, 1), date(2014, 2, 2)),
                         relativedelta(months=-1, days=-1, bdays=-22))
        self.assertEqual(relativedelta(datetime(2017, 1, 16),
                                       datetime(2017, 1, 16),
                                       holidays=holidays.US()),
                         relativedelta(bdays=0))
        self.assertEqual(relativedelta(datetime(2017, 1, 17),
                                       datetime(2017, 1, 16),
                                       holidays=holidays.US()),
                         relativedelta(days=1, bdays=0))

    def test_init_time(self):
        self.assertEqual(relativedelta(datetime(2015, 1, 5, 9, 15),
                                       datetime(2015, 1, 2, 16, 45)),
                         relativedelta(days=2, hours=16, minutes=30,
                                       bminutes=30))
        self.assertEqual(relativedelta(datetime(2015, 1, 20, 21, 22),
                                       datetime(2015, 1, 9, 3, 0)),
                         relativedelta(days=11, hours=18, minutes=22,
                                       bdays=7, bhours=8, bminutes=0))
        self.assertEqual(relativedelta(datetime(2015, 1, 20, 21, 22),
                                       datetime(2015, 1, 9, 3, 0),
                                       holidays=holidays.US()),
                         relativedelta(days=11, hours=18, minutes=22,
                                       bdays=6, bhours=8, bminutes=0))
        bdateutil.HOLIDAYS = holidays.CA()
        self.assertEqual(relativedelta(datetime(2015, 1, 20, 21, 22),
                                       datetime(2015, 1, 9, 3, 0)),
                         relativedelta(days=11, hours=18, minutes=22,
                                       bdays=7, bhours=8, bminutes=0))
        bdateutil.HOLIDAYS = []
        self.assertEqual(relativedelta(time(3, 40), time(2, 37)),
                         relativedelta(hours=1, minutes=3))

    def test_add(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4,
                            bhours=+5, bminutes=+6, bseconds=+7,
                            hours=+8, minutes=+9, seconds=+10)
        rd2 = relativedelta(years=+10, months=-9, bdays=+8, days=-7,
                            bhours=+6, bminutes=-5, bseconds=+4,
                            hours=-3, minutes=+2, seconds=-1)
        rd3 = relativedelta(years=+11, months=-7, bdays=+11, days=-3,
                            bhours=+11, bminutes=+1, bseconds=+11,
                            hours=+5, minutes=+11, seconds=+9)
        self.assertEqual(rd1 + rd2, rd3)
        self.assertEqual(relativedelta(bdays=3) + date(2014, 1, 3),
                         date(2014, 1, 8))
        rd4 = relativedelta(years=+1, months=+2, days=+1)
        rd5 = relativedelta(years=+12, months=-5, bdays=+11, days=-2,
                            bhours=+11, bminutes=+1, bseconds=+11,
                            hours=+5, minutes=+11, seconds=+9)
        self.assertEqual(rd3 + rd4, rd5)
        self.assertEqual(date("2014-01-01") + relativedelta(weekday=FR),
                         date(2014, 1, 3))
        self.assertEqual(datetime("2014-11-15 1:23") + relativedelta(bdays=1),
                         datetime(2014, 11, 18, 1, 23))

    def test_add_sub(self):
        self.assertEqual(datetime("2014-11-15 1:23").add(bdays=1),
                         datetime(2014, 11, 18, 1, 23))
        self.assertEqual(datetime("2014-11-15 1:23").sub(bdays=-1),
                         datetime(2014, 11, 18, 1, 23))
        self.assertEqual(date(2016, 1, 1).add(hours=2, minutes=4),
                         datetime(2016, 1, 1, 2, 4))
        self.assertEqual(datetime(2016, 1, 1, 0).sub(days=1),
                         datetime(2015, 12, 31, 0))
        ush = holidays.US()
        self.assertEqual(date(2016, 12, 30).add(bdays=1, holidays=ush),
                         date(2017, 1, 3))
        self.assertEqual(date(2016, 12, 31).add(bdays=0, holidays=ush),
                         date(2017, 1, 3))
        self.assertEqual(date(2016, 12, 31).add(bdays=1, holidays=ush),
                         date(2017, 1, 4))
        self.assertEqual(time(3, 40).add(hours=5, minutes=25), time(9, 5))

    def test_start_end(self):
        dt = datetime(2016, 12, 30, 5)
        self.assertEqual(dt.day_start(), datetime(2016, 12, 30, 0))
        self.assertEqual(dt.day_end(),
                         datetime(2016, 12, 30, 23, 59, 59, 999999))
        self.assertEqual(dt.month_start(), datetime(2016, 12, 1, 0))
        self.assertEqual(dt.month_end(),
                         datetime(2016, 12, 31, 23, 59, 59, 999999))
        self.assertEqual(dt.year_start(), datetime(2016, 1, 1, 0))
        self.assertEqual(dt.year_end(),
                         datetime(2016, 12, 31, 23, 59, 59, 999999))
        d = date(2015, 2, 13)
        self.assertEqual(d.month_start(), date(2015, 2, 1))
        self.assertEqual(d.month_end(), date(2015, 2, 28))
        self.assertEqual(d.year_start(), date(2015, 1, 1))
        self.assertEqual(d.year_end(), date(2015, 12, 31))

    def test_bdays_zero(self):
        self.assertEqual(date("2014-11-15") + relativedelta(bdays=0),
                         date(2014, 11, 17))
        self.assertEqual(date("2014-11-17") + relativedelta(bdays=0),
                         date(2014, 11, 17))
        self.assertEqual(date("2014-11-15") - relativedelta(bdays=0),
                         date(2014, 11, 14))
        self.assertEqual(date("2014-11-14") - relativedelta(bdays=0),
                         date(2014, 11, 14))

    def test_radd(self):
        self.assertEqual(date(2014, 1, 3) + relativedelta(bdays=2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 1, 7) + relativedelta(bdays=-2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 2, 3) + relativedelta(bdays=-19),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 1, 3) + relativedelta(bdays=1.5),
                         datetime(2014, 1, 6, 13, 0))

    def test_radd_time(self):
        self.assertEqual(datetime("2015-01-02 16:45") +
                         relativedelta(bminutes=+30),
                         datetime(2015, 1, 5, 9, 15))
        self.assertEqual(date(2015, 1, 2) + relativedelta(bminutes=+30),
                         datetime(2015, 1, 2, 9, 30))
        self.assertEqual(date(2014, 1, 3) + relativedelta(bdays=1, bhours=4),
                         datetime(2014, 1, 6, 13, 0))
        bdateutil.BTSTART = time(7, 30)
        self.assertEqual(datetime("2015-01-02 16:45") +
                         relativedelta(bminutes=+30),
                         datetime(2015, 1, 5, 7, 45))
        self.assertEqual(datetime("2015-01-02 16:45") +
                         relativedelta(bhours=+0.5),
                         datetime(2015, 1, 5, 7, 45))
        bdateutil.BTSTART = time(9, 0)

    def test_sub(self):
        rd1 = relativedelta(years=+1, months=+2, bdays=+3, days=+4,
                            bhours=+5, bminutes=+6, bseconds=+7,
                            hours=+8, minutes=+9, seconds=+10)
        rd2 = relativedelta(years=+10, months=-9, bdays=+8, days=-7,
                            bhours=+6, bminutes=-5, bseconds=+4,
                            hours=-3, minutes=+2, seconds=-1)
        rd3 = relativedelta(years=-9, months=+11, bdays=-5, days=+11,
                            bhours=-1, bminutes=+11, bseconds=+3,
                            hours=+11, minutes=+7, seconds=+11)
        self.assertEqual(rd1 - rd2, rd3)

    def test_rsub(self):
        self.assertEqual(date(2014, 1, 7) - relativedelta(bdays=2),
                         date(2014, 1, 3))
        self.assertEqual(date(2014, 1, 3) - relativedelta(bdays=-2),
                         date(2014, 1, 7))
        self.assertEqual(date(2014, 2, 3) - relativedelta(bdays=19),
                         date(2014, 1, 7))
        self.assertEqual(date("2014-11-15") - relativedelta(bdays=1),
                         date(2014, 11, 14))
        self.assertEqual(date.today() - relativedelta(bdays=+45),
                         date.today() + relativedelta(bdays=-45))

    def test_neg(self):
        self.assertEqual(-relativedelta(years=+1, bdays=-3),
                         relativedelta(years=-1, bdays=+3))

    def test_bool(self):
        self.assertTrue(relativedelta(bdays=1))
        self.assertTrue(relativedelta(days=1))
        self.assertFalse(relativedelta())

    def test_mul(self):
        self.assertEqual(relativedelta(years=+1, bdays=-3) * 3,
                         relativedelta(years=+3, bdays=-9))
        self.assertEqual(relativedelta(years=+1, bdays=-3) * -3,
                         relativedelta(years=-3, bdays=+9))
        self.assertEqual(relativedelta(years=+1, bdays=-3) * 0,
                         relativedelta(years=0, bdays=0))

    def test_rmul(self):
        self.assertEqual(3 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=+3, bdays=-9))
        self.assertEqual(-3 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=-3, bdays=+9))
        self.assertEqual(0 * relativedelta(years=+1, bdays=-3),
                         relativedelta(years=0, bdays=0))

    def test_eq(self):
        r1 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        r2 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        self.assertEqual(r1, r2)
        self.assertTrue(r1 == r2)
        r2.days = 4
        self.assertNotEqual(r1, r2)
        self.assertFalse(r1 == r2)
        r2.days = 3
        r2.bdays = 0
        self.assertNotEqual(r1, r2)
        self.assertFalse(r1 == r2)
        self.assertEqual(relativedelta(), relativedelta())
        self.assertTrue(relativedelta() == relativedelta())
        self.assertNotEqual(relativedelta(days=1), relativedelta(bdays=1))
        self.assertFalse(relativedelta() == relativedelta(months=1))
        self.assertNotEqual(relativedelta(days=1), relativedelta(bdays=1))
        self.assertFalse(relativedelta() == relativedelta(months=1))

    def test_ne(self):
        r1 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        r2 = relativedelta(years=1, months=2, days=3, bdays=1,
                           hours=4, minutes=5, seconds=6, microseconds=7)
        self.assertFalse(r1 != r2)
        r2.days = 4
        self.assertTrue(r1 != r2)
        r2.days = 3
        r2.bdays = 0
        self.assertTrue(r1 != r2)
        self.assertFalse(relativedelta() != relativedelta())
        self.assertTrue(relativedelta() != relativedelta(months=1))
        self.assertTrue(relativedelta() != relativedelta(months=1))

    def test_div(self):
        self.assertEqual(relativedelta(years=+3, bdays=-9) / 3,
                         relativedelta(years=+1, bdays=-3))
        self.assertEqual(relativedelta(years=+3, bdays=-9) / -3,
                         relativedelta(years=-1, bdays=+3))
        self.assertRaises(ZeroDivisionError,
                          lambda: relativedelta(bdays=-3) / 0)

    def test_truediv(self):
        self.assertEqual(relativedelta(years=+4, bdays=-10) / 3.0,
                         relativedelta(years=+1, bdays=-3))

    def test_repr(self):
        rd1 = relativedelta(years=+1, months=+2, days=-3)
        self.assertEqual(str(rd1),
                         "relativedelta(years=+1, months=+2, days=-3)")
        rd2 = relativedelta(years=+1, months=+2, bdays=-7)
        self.assertEqual(str(rd2),
                         "relativedelta(years=+1, months=+2, bdays=-7)")
        rd3 = relativedelta(years=-1, months=-2, bdays=+7)
        self.assertEqual(str(rd3),
                         "relativedelta(years=-1, months=-2, bdays=+7)")
        rd4 = relativedelta(year=2014, month=1, day=2)
        self.assertEqual(str(rd4),
                         "relativedelta(year=2014, month=1, day=2)")


class TestParser(unittest.TestCase):

    def test_timestamp(self):
        self.assertEqual(parse(1388577600).date(), date(2014, 1, 1))

    def test_parserinfo(self):
        self.assertEqual(parse("1/2/2014"), datetime(2014, 1, 2))
        self.assertEqual(parse(b"1/2/2014"), datetime(2014, 1, 2))
        self.assertEqual(parse("1/2/2014", dayfirst=True),
                         datetime(2014, 2, 1))
        self.assertEqual(parse("1/2/2014", parserinfo(dayfirst=True)),
                         datetime(2014, 2, 1))

    def test_exceptions(self):
        self.assertRaises(ValueError, lambda: parse("abc"))
        self.assertRaises(TypeError, lambda: parse(['a', 'b', 'c']))


class TestRRule(unittest.TestCase):

    def test_bdaily(self):
        start = parse("2014-01-01")
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart=start)),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0),
                          datetime(2014, 1, 6, 0, 0)])
        until = parse("2014-01-09")
        self.assertEqual(list(rrule(BDAILY, dtstart=start, until=until)),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0),
                          datetime(2014, 1, 6, 0, 0),
                          datetime(2014, 1, 7, 0, 0),
                          datetime(2014, 1, 8, 0, 0),
                          datetime(2014, 1, 9, 0, 0)])

    def test_parse(self):
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2014-01-01")),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0),
                          datetime(2014, 1, 6, 0, 0)])
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2014-01-01",
                                    until="01/04/2014")),
                         [datetime(2014, 1, 1, 0, 0),
                          datetime(2014, 1, 2, 0, 0),
                          datetime(2014, 1, 3, 0, 0)])

    def test_holidays(self):
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2015-07-01")),
                         [datetime(2015, 7, 1, 0, 0),
                          datetime(2015, 7, 2, 0, 0),
                          datetime(2015, 7, 3, 0, 0),
                          datetime(2015, 7, 6, 0, 0)])
        bdateutil.HOLIDAYS = holidays.US()
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2015-07-01")),
                         [datetime(2015, 7, 1, 0, 0),
                          datetime(2015, 7, 2, 0, 0),
                          datetime(2015, 7, 6, 0, 0),
                          datetime(2015, 7, 7, 0, 0)])
        self.assertEqual(list(rrule(BDAILY, count=4, dtstart="2015-07-01",
                              holidays=holidays.CA())),
                         [datetime(2015, 7, 2, 0, 0),
                          datetime(2015, 7, 3, 0, 0),
                          datetime(2015, 7, 6, 0, 0),
                          datetime(2015, 7, 7, 0, 0)])
        bdateutil.HOLIDAYS = []


class TestDateTime(unittest.TestCase):

    def test_date(self):
        self.assertEqual(date("2015-03-25"), dt.date(2015, 3, 25))
        self.assertEqual(date("1/2/2014"), dt.date(2014, 1, 2))
        self.assertEqual(date(1388577600), dt.date(2014, 1, 1))
        self.assertRaises(ValueError, lambda: date("abc"))
        self.assertRaises(TypeError, lambda: date(['a', 'b', 'c']))
        self.assertRaises(TypeError, lambda: date(time(3, 40)))
        self.assertEqual(date(2015, 2, 15).month_end(), date(2015, 2, 28))
        self.assertEqual(date.today(), dt.date.today())
        self.assertEqual(date.today(days=+1),
                         dt.date.today() + relativedelta(days=+1))
        self.assertEqual(date.today(bdays=+200, holidays=holidays.US()),
                         dt.date.today() +
                         relativedelta(bdays=+200, holidays=holidays.US()))
        relativedelta.holidays = holidays.US()
        self.assertEqual(date.today(bdays=+200),
                         dt.date.today() + relativedelta(bdays=+200))
        del relativedelta.holidays

    def test_datetime(self):
        self.assertEqual(datetime("2015-03-25 12:34"),
                         dt.datetime(2015, 3, 25, 12, 34))
        self.assertEqual(datetime(2015, 3, 15, 23, 45).month_end(),
                         datetime(2015, 3, 31, 23, 59, 59, 999999))
        self.assertEqual(datetime.now().date(), dt.datetime.now().date())
        self.assertEqual(datetime.now(bdays=-45).date(),
                         (dt.datetime.now() - relativedelta(bdays=45)).date())
        self.assertEqual(datetime(time("3:40")),
                         dt.datetime.combine(dt.datetime.today(),
                                             dt.time(3, 40, 0)))

    def test_time(self):
        self.assertEqual(time("12:45:54"), time(12, 45, 54))
        self.assertEqual(time("2:30 PM"), time(14, 30))
        self.assertEqual(relativedelta(time("3:40"), time(2, 30)),
                         relativedelta(hours=1, minutes=10))
        self.assertEqual(relativedelta("3:40", time(2, 30)),
                         relativedelta(hours=1, minutes=10))
        self.assertEqual(relativedelta(time(2, 30), time(3, 40)),
                         relativedelta(hours=-1, minutes=-10))

    def test_week(self):
        self.assertEqual(date("2016-12-20").week, 51)


class TestDefaults(unittest.TestCase):

    def test_WORKDAYS(self):
        self.assertEqual(date(2017, 1, 4) + relativedelta(bdays=3),
                         date(2017, 1, 9))
        bdateutil.WORKDAYS = (0, 1, 2)  # Mon, Tues, Wed
        self.assertEqual(date(2017, 1, 4) + relativedelta(bdays=3),
                         date(2017, 1, 11))
        self.assertEqual(date(2017, 1, 4) + relativedelta(bdays=3,
                                                          workdays=(0,)),
                         date(2017, 1, 30))
        bdateutil.WORKDAYS = range(5)
        self.assertRaises(ValueError,
                          lambda: date(2017, 1, 4) +
                          relativedelta(bdays=3, workdays=()))
        self.assertRaises(ValueError,
                          lambda: date(2017, 1, 4) +
                          relativedelta(bdays=3, workdays=('x', 'y')))

    def test_BTSTART_BTEND(self):
        self.assertEqual(time(16, 30) + relativedelta(bminutes=60),
                         time(9, 30))
        bdateutil.BTSTART = time(10, 30)
        bdateutil.BTEND = time(16, 45)
        self.assertEqual(time(16, 30) + relativedelta(bminutes=60),
                         time(11, 15))
        self.assertEqual(time(16, 30) + relativedelta(bminutes=60,
                                                      btstart=time(11, 30)),
                         time(12, 15))
        bdateutil.BTEND = time(8, 0)
        self.assertRaises(ValueError,
                          lambda: time(16, 30) + relativedelta(bminutes=60))
        bdateutil.BTEND = None
        self.assertRaises(TypeError,
                          lambda: time(16, 30) + relativedelta(bminutes=60))
        bdateutil.BTSTART = time(9, 0)
        bdateutil.BTEND = time(17, 0)


if __name__ == "__main__":
    unittest.main(failfast=True)
