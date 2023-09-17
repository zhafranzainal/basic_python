import unittest
from datetime import datetime
from sorting_timestamps import extract_distinct_dates, find_consecutive_sequences


class TestLoginSequences(unittest.TestCase):

    def test_extract_distinct_dates(self):
        timestamps = [
            '2021-03-13 15:13:05', '2021-03-13 23:13:05', '2021-03-16 15:13:05',
            '2021-03-16 23:13:05', '2021-03-17 07:13:05', '2021-03-17 15:13:05',
            '2021-03-17 23:13:05', '2021-03-18 07:13:05', '2021-03-18 15:13:05'
        ]

        expected_dates = [datetime(2021, 3, 13), datetime(2021, 3, 16), datetime(2021, 3, 17), datetime(2021, 3, 18)]

        self.assertEqual(extract_distinct_dates(timestamps), expected_dates)

    def test_find_consecutive_sequences(self):
        dates = [datetime(2021, 3, 13), datetime(2021, 3, 16), datetime(2021, 3, 17), datetime(2021, 3, 18)]

        expected_sequences = [(datetime(2021, 3, 16), datetime(2021, 3, 18), 3),
                              (datetime(2021, 3, 13), datetime(2021, 3, 13), 1)]

        self.assertEqual(find_consecutive_sequences(dates), expected_sequences)


if __name__ == '__main__':
    unittest.main()
