import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class ImportEasterTest(unittest.TestCase):
    """ Test that bdateutil.easter-related imports work properly """

    def testEasterDirect(self):
        import bdateutil.easter

    def testEasterFrom(self):
        from bdateutil import easter

    def testEasterStar(self):
        from bdateutil.easter import easter


class ImportParserTest(unittest.TestCase):
    """ Test that bdateutil.parser-related imports work properly """
    def testParserDirect(self):
        import bdateutil.parser

    def testParserFrom(self):
        from bdateutil import parser

    def testParserAll(self):
        # All interface
        from bdateutil.parser import parse
        from bdateutil.parser import parserinfo

        # Other public classes
        from bdateutil.parser import parser

        for var in (parse, parserinfo, parser):
            self.assertIsNot(var, None)


class ImportRelativeDeltaTest(unittest.TestCase):
    """ Test that bdateutil.relativedelta-related imports work properly """
    def testRelativeDeltaDirect(self):
        import bdateutil.relativedelta

    def testRelativeDeltaFrom(self):
        from bdateutil import relativedelta

    def testRelativeDeltaAll(self):
        from bdateutil.relativedelta import relativedelta
        from bdateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU

        for var in (relativedelta, MO, TU, WE, TH, FR, SA, SU):
            self.assertIsNot(var, None)

        # In the public interface but not in all
        from bdateutil.relativedelta import weekday
        self.assertIsNot(weekday, None)


class ImportRRuleTest(unittest.TestCase):
    """ Test that bdateutil.rrule related imports work properly """
    def testRRuleDirect(self):
        import bdateutil.rrule

    def testRRuleFrom(self):
        from bdateutil import rrule

    def testRRuleAll(self):
        from bdateutil.rrule import rrule
        from bdateutil.rrule import rruleset
        from bdateutil.rrule import rrulestr
        from bdateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY
        from bdateutil.rrule import HOURLY, MINUTELY, SECONDLY
        from bdateutil.rrule import MO, TU, WE, TH, FR, SA, SU

        rr_all = (rrule, rruleset, rrulestr,
                  YEARLY, MONTHLY, WEEKLY, DAILY,
                  HOURLY, MINUTELY, SECONDLY,
                  MO, TU, WE, TH, FR, SA, SU)

        for var in rr_all:
            self.assertIsNot(var, None)

        # In the public interface but not in all
        from bdateutil.rrule import weekday
        self.assertIsNot(weekday, None)


class ImportTZTest(unittest.TestCase):
    """ Test that bdateutil.tz related imports work properly """
    def testTzDirect(self):
        import bdateutil.tz

    def testTzFrom(self):
        from bdateutil import tz

    def testTzAll(self):
        from bdateutil.tz import tzutc
        from bdateutil.tz import tzoffset
        from bdateutil.tz import tzlocal
        from bdateutil.tz import tzfile
        from bdateutil.tz import tzrange
        from bdateutil.tz import tzstr
        from bdateutil.tz import tzical
        from bdateutil.tz import gettz
        from bdateutil.tz import tzwin
        from bdateutil.tz import tzwinlocal

        tz_all = ["tzutc", "tzoffset", "tzlocal", "tzfile", "tzrange",
                  "tzstr", "tzical", "gettz"]

        tz_all += ["tzwin", "tzwinlocal"] if sys.platform.startswith("win") else []
        lvars = locals()

        for var in tz_all:
            self.assertIsNot(lvars[var], None)


@unittest.skipUnless(sys.platform.startswith('win'), "Requires Windows")
class ImportTZWinTest(unittest.TestCase):
    """ Test that bdateutil.tzwin related imports work properly """
    def testTzwinDirect(self):
        import bdateutil.tzwin

    def testTzwinFrom(self):
        from bdateutil import tzwin

    def testTzwinStar(self):
        tzwin_all = ["tzwin", "tzwinlocal"]


class ImportZoneInfoTest(unittest.TestCase):
    def testZoneinfoDirect(self):
        import bdateutil.zoneinfo

    def testZoneinfoFrom(self):
        from bdateutil import zoneinfo

    def testZoneinfoStar(self):
        from bdateutil.zoneinfo import gettz
        from bdateutil.zoneinfo import gettz_db_metadata
        from bdateutil.zoneinfo import rebuild

        zi_all = (gettz, gettz_db_metadata, rebuild)

        for var in zi_all:
            self.assertIsNot(var, None)
