from datetime import datetime

import argparse
import re


def add_timestamp(filename):
    # validate filename input
    valid_filenames = ("wavedata.txt", "gendata.txt")
    if filename not in valid_filenames:
        raise ValueError(f"{filename} is not one of the valid filenames: {valid_filenames}")

    file = open(f"./surf/{filename}")
    content = file.readlines()
    timestamp = datetime.now().strftime("%m/%d/%y %H:%M")  # get timestamp
    if "TIMESTAMP" in content[0]:  # if timestamp is already there, just update the value
        timestamp_pattern = re.compile(r"\d{2}/\d{2}/\d{2}\s\d{2}:\d{2}\sPST")
        content[2] = re.sub(timestamp_pattern, f"{timestamp} PST", content[2])  # datetime.now() returns local time, so assume PST
    else:  # if timestamp is not there, create new column for timestamp
        content[0] = content[0].strip() + "   TIMESTAMP\n"
        content[1] = content[1].strip() + "  MM/DD/YY hh:mm TZ\n"
        content[2] = content[2].strip() + f"   {timestamp} PST\n"  # datetime.now() returns local time, so assume PST
    data = content[0]+content[1]+content[2]
    with open(f"./surf/{filename}", "w") as f:
        f.write(data)
    print(data)
    f.close


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--name", help="Name of noaa file to add timestamp to", required=True)
    args = parser.parse_args()

    add_timestamp(args.name)