import unittest
from datetime import datetime
from sorting_timestamps import extract_distinct_dates, find_consecutive_sequences


class TestSortingTimestamps(unittest.TestCase):

    def setUp(self):
        self.distinct_dates = [
            datetime(2021, 3, 13), datetime(2021, 3, 16), datetime(2021, 3, 17), datetime(2021, 3, 18)
        ]

    def test_extract_distinct_dates_valid(self):
        """Test extracting distinct dates from valid timestamps."""

        timestamps = [
            '2021-03-13 15:13:05', '2021-03-13 23:13:05', '2021-03-16 15:13:05',
            '2021-03-16 23:13:05', '2021-03-17 07:13:05', '2021-03-17 15:13:05',
            '2021-03-17 23:13:05', '2021-03-18 07:13:05', '2021-03-18 15:13:05'
        ]

        self.assertEqual(extract_distinct_dates(timestamps), self.distinct_dates)

    def test_extract_distinct_dates_empty(self):
        """Test extracting distinct dates from an empty list."""
        self.assertEqual(extract_distinct_dates([]), [])

    def test_extract_distinct_dates_invalid(self):
        """Test extracting distinct dates from timestamps with invalid format."""

        invalid_timestamps = [
            '2023-11-11 01:17:12', '2023-10-07 08:17:12', 'asdasd', 'asdasd', 'asdasd', 'asdasd', '2023-10-25 03:17:12',
            'asdasd', 'asdasd', 'asdasd', '2023-10-03 00:17:12', '2023-11-05 08:17:12', 'asdasd', 'asdasd', 'asdasd',
            '2023-11-01 08:17:12', 'asdasd', 'asdasd', '2023-10-19 01:17:12', '2023-11-13 05:17:12', 'asdasd', 'asdasd',
            '2023-11-02 09:17:12', 'asdasd', '2023-11-10 02:17:12', '2023-09-23 11:17:12', '2023-10-06 13:17:12',
            'asdasd', '2023-10-04 01:17:12', '2023-10-11 17:17:12', 'asdasd', '2023-10-05 11:17:12',
            '2023-11-09 02:17:12', 'asdasd', '2023-09-18 19:17:12', '2023-11-16 17:17:12', '2023-10-01 19:17:12',
            'asdasd', '2023-09-22 10:17:12', 'asdasd', 'asdasd', '2023-10-22 03:17:12', 'asdasd', 'asdasd',
            '2023-09-25 06:17:12', '2023-11-04 12:17:12', '2023-10-22 10:17:12'
        ]

        expected_dates = [
            datetime(2023, 9, 18), datetime(2023, 9, 22), datetime(2023, 9, 23), datetime(2023, 9, 25),
            datetime(2023, 10, 1), datetime(2023, 10, 3), datetime(2023, 10, 4), datetime(2023, 10, 5),
            datetime(2023, 10, 6), datetime(2023, 10, 7), datetime(2023, 10, 11), datetime(2023, 10, 19),
            datetime(2023, 10, 22), datetime(2023, 10, 25), datetime(2023, 11, 1), datetime(2023, 11, 2),
            datetime(2023, 11, 4), datetime(2023, 11, 5), datetime(2023, 11, 9), datetime(2023, 11, 10),
            datetime(2023, 11, 11), datetime(2023, 11, 13), datetime(2023, 11, 16)
        ]

        self.assertEqual(extract_distinct_dates(invalid_timestamps), expected_dates)

    def test_find_consecutive_sequences_valid(self):
        """Test finding consecutive sequences from a valid list of dates."""

        expected_sequences = [
            (datetime(2021, 3, 16), datetime(2021, 3, 18), 3),
            (datetime(2021, 3, 13), datetime(2021, 3, 13), 1)
        ]

        self.assertEqual(find_consecutive_sequences(self.distinct_dates), expected_sequences)

    def test_find_consecutive_sequences_empty(self):
        """Test finding consecutive sequences from an empty list of dates."""
        self.assertEqual(find_consecutive_sequences([]), [])

    def test_find_consecutive_sequences_single_date(self):
        """Test finding consecutive sequences from a list with a single date."""

        single_date = datetime(2021, 3, 13)
        expected_sequences = [(single_date, single_date, 1)]

        self.assertEqual(find_consecutive_sequences([single_date]), expected_sequences)


if __name__ == '__main__':
    unittest.main()
