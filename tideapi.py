import urequests
import json
import utime
import sys


def fetchData():
    # Get the current local time
    current_time = utime.localtime()

    # Format the date as 'yyyy-mm-dd'
    formatted_date = "{:04d}-{:02d}-{:02d}".format(
        current_time[0], current_time[1], current_time[2])

    print("Current date:", formatted_date)

    # API endpoint
    url = "https://api.niwa.co.nz/tides/data"

    # Query Parameters
    params = {
        "lat": "-36.58868088701637",
        "long": "174.70479819",
        "numberOfDays": 3,
        "startDate": formatted_date,
    }

    # Construct the full URL with query parameters
    query_string = "&".join(f"{key}={value}" for key, value in params.items())
    url_with_params = f"{url}?{query_string}"

    # Headers
    headers = {
        "x-apikey": "8hAo6Pg4RTxhnq8o147p0SznPafHQuut",  # Replace with your API key
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = urequests.get(url_with_params, headers=headers)

        tide_data = json.loads(response.content)  # Parse JSON

        # print("json", tide_data)
        # print("txt", response.text)

    except Exception as e:
        sys.print_exception(e)
    finally:
        if 'response' in locals():
            response.close()

        # print("API request completed.")

        return tide_data


def iso_to_epoch(iso_time):
    # Parse the time string (UTC) into components
    year = int(iso_time[0:4])
    month = int(iso_time[5:7])
    day = int(iso_time[8:10])
    hour = int(iso_time[11:13])
    minute = int(iso_time[14:16])
    second = int(iso_time[17:19])

    # Convert to epoch timestamp
    return utime.mktime((year, month, day, hour, minute, second, 0, 0))


def processData(tide_data):
    # Initialize variables
    first_greater = None
    last_less = None

    # to offset the time
    # current_time = utime.time() + (9 * 60 * 60)
    current_time = utime.time()

    # Iterate through the values
    for entry in tide_data['values']:
        entry_time = iso_to_epoch(entry['time'])

        if entry_time > current_time and first_greater is None:
            first_greater = entry
        if entry_time < current_time:
            last_less = entry

    # Calculate the difference in minutes
    if first_greater and last_less:
        first_greater_time = iso_to_epoch(first_greater['time'])
        last_less_time = iso_to_epoch(last_less['time'])
        # difference_seconds = first_greater_time - last_less_time
        # difference_minutes = difference_seconds // 60
        # print(f"Time Difference: {difference_minutes} minutes")

    # Return a tuple, the percentage first, then the boolean for the direction.
    return ((current_time-last_less_time) /
            (first_greater_time - last_less_time), first_greater['value'] < last_less['value'])
