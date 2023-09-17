"""
Problem Statement:

Given a list of timestamps representing login times generated by 'seed.py'. The problem stems from needing to award
badges for consecutive logins. The 'length' of consecutive logins is defined as the number of consecutive days with
login activity, NOT the total number of consecutive logins. The task is to output a table that displays timestamps
sorted by consecutive logins (length) in descending order.
"""

from datetime import datetime, timedelta
from typing import List, Tuple


def extract_distinct_dates(timestamps: List[str]) -> List[datetime]:
    """
    Extract distinct dates from a list of timestamps and return them as datetime objects.

    Args:
        timestamps (List[str]): List of timestamps in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
        List[datetime]: List of distinct dates as datetime objects, sorted in ascending order.
    """
    distinct_dates = set()

    for timestamp in timestamps:
        try:
            date_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            date_str = date_obj.strftime('%Y-%m-%d')
            distinct_dates.add(date_str)
        except ValueError:
            continue  # Skip dirty data

    distinct_dates_list = sorted(list(distinct_dates))

    # Convert distinct_dates_list to datetime objects
    return [datetime.strptime(date, "%Y-%m-%d") for date in distinct_dates_list]


def find_consecutive_sequences(dates: List[datetime]) -> List[Tuple[datetime, datetime, int]]:
    """
    Find consecutive sequences of dates with login activity.

    Args:
        dates (List[datetime]): List of distinct dates as datetime objects.

    Returns:
        List[Tuple[datetime, datetime, int]]: List of consecutive sequences, each containing
        a start date, end date, and length of the sequence.
    """
    sequences = []
    current_start = dates[0]
    current_end = dates[0]
    current_length = 1

    # Iterate through the dates to find all consecutive sequences
    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            current_end = dates[i]
            current_length += 1
        else:
            sequences.append((current_start, current_end, current_length))
            current_start = dates[i]
            current_end = dates[i]
            current_length = 1

    # Append the last sequence
    sequences.append((current_start, current_end, current_length))

    # Sort the sequences in descending order by length, and then by start date
    return sorted(sequences, key=lambda x: (-x[2], -x[0].timestamp()))


def print_sequences_table(sequences: List[Tuple[datetime, datetime, int]]) -> None:
    """
    Print consecutive sequences as a table.

    Args:
        sequences (List[Tuple[datetime, datetime, int]]): List of consecutive sequences.
    """
    print("\n| START      | END        | LENGTH |")
    print("|------------|------------|--------|")

    for sequence in sequences:
        start, end, length = sequence
        print(f"| {start.strftime('%Y-%m-%d')} | {end.strftime('%Y-%m-%d')} | {length:>6} |")


def main():
    # Import generated timestamps from seed.py
    from seed import res

    dates = extract_distinct_dates(res)
    sequences = find_consecutive_sequences(dates)
    print_sequences_table(sequences)


if __name__ == "__main__":
    main()
