from datetime import datetime, timedelta
from random import randint, random, sample


def generate_random_timestamps(start_date, end_date):
    result = []
    current_date = start_date

    while current_date < end_date:
        if random() > 0.5:
            result.append(current_date.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            result.append('asdasd')

        high_rand = randint(24, 72)
        low_rand = randint(5, 18)
        value = randint(low_rand, high_rand)
        step = timedelta(hours=value)
        current_date += step

    return sample(result, len(result))


# Define the start and end date
start_date = datetime.now()
end_date = start_date + timedelta(days=60)

# Call the function to generate timestamps
timestamps = generate_random_timestamps(start_date, end_date)

# Create an empty set to store distinct dates
distinct_dates = set()

# Convert timestamps to datetime objects and extract the date component
for timestamp in timestamps:
    try:
        date_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        date_str = date_obj.strftime('%Y-%m-%d')
        distinct_dates.add(date_str)
    except ValueError:
        continue  # Skip 'asdasd' entries

# Convert the set back to a sorted list if needed
distinct_dates_list = sorted(list(distinct_dates))

# Convert distinct_dates_list to datetime objects
dates = [datetime.strptime(date, "%Y-%m-%d") for date in distinct_dates_list]

# Sort the dates in ascending order
dates.sort()

# Initialize variables to track the current consecutive sequence
current_start = dates[0]
current_end = dates[0]
max_start = dates[0]
max_end = dates[0]
max_length = 1
current_length = 1

# Iterate through the dates to find the longest consecutive sequence
for i in range(1, len(dates)):
    if dates[i] - dates[i - 1] == timedelta(days=1):
        current_end = dates[i]
        current_length += 1
    else:
        if current_length > max_length:
            max_length = current_length
            max_start = current_start
            max_end = current_end
        current_start = dates[i]
        current_end = dates[i]
        current_length = 1

# Check if the last sequence is the longest
if current_length > max_length:
    max_length = current_length
    max_start = current_start
    max_end = current_end

# Print the table
print()
print("| START      | END        | LENGTH |")
print("|------------|------------|--------|")
print(f"| {max_start.strftime('%Y-%m-%d')} | {max_end.strftime('%Y-%m-%d')} | {max_length:^6} |")
