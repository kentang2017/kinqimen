import datetime
import unittest

from config import _calendar_days_since_jieqi


class ZhirunDayOffsetTests(unittest.TestCase):
    def test_time_after_jieqi_on_same_date_is_day_zero(self):
        jieqi_start = datetime.datetime(2026, 6, 21, 16, 0)
        current = datetime.datetime(2026, 6, 21, 23, 59)

        self.assertEqual(_calendar_days_since_jieqi(current, jieqi_start), 0)

    def test_next_calendar_date_is_day_one(self):
        jieqi_start = datetime.datetime(2026, 6, 21, 16, 0)
        current = datetime.datetime(2026, 6, 22, 0, 1)

        self.assertEqual(_calendar_days_since_jieqi(current, jieqi_start), 1)

    def test_day_offset_counts_calendar_dates(self):
        jieqi_start = datetime.datetime(2026, 12, 31, 23, 59)
        current = datetime.datetime(2027, 1, 2, 0, 1)

        self.assertEqual(_calendar_days_since_jieqi(current, jieqi_start), 2)


if __name__ == "__main__":
    unittest.main()
