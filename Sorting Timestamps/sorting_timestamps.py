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

# Print the distinct dates
for date in distinct_dates_list:
    print(date)
