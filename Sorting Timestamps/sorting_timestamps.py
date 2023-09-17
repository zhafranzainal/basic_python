from seed import res
from datetime import datetime, timedelta

# Access timestamps list generated in seed.py
timestamps = res

# Create an empty set to store distinct dates
distinct_dates = set()

# Convert timestamps to datetime objects and extract the date component
for timestamp in timestamps:
    try:
        date_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        date_str = date_obj.strftime('%Y-%m-%d')
        distinct_dates.add(date_str)
    except ValueError:
        continue  # Skip dirty data

# Convert the set back to a sorted list if needed
distinct_dates_list = sorted(list(distinct_dates))

# Convert distinct_dates_list to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%d") for date in distinct_dates_list]

# Sort the dates in ascending order
dates.sort()

# Initialize variables to track the consecutive sequences
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

# Sort the sequences first by length in descending order, and then by start date in descending order
sequences.sort(key=lambda x: (-x[2], -x[0].timestamp()))

# Print the table
print()
print("| START      | END        | LENGTH |")
print("|------------|------------|--------|")

for sequence in sequences:
    start, end, length = sequence
    print(f"| {start.strftime('%Y-%m-%d')} | {end.strftime('%Y-%m-%d')} | {length:>6} |")
