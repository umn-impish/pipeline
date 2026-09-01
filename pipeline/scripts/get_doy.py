#!/usr/bin/env python

import argparse
from datetime import datetime


def main():

    parser = argparse.ArgumentParser(
        description="Get the day-of-year (DOY) from the provided date in YYYY-MM-DD format",
        epilog="Example of use: python convert_to_doy 2026-06-25",
    )
    _ = parser.add_argument("date", type=str, help="in YYYY-MM-DD format")
    arg = parser.parse_args()
    print(datetime.strptime(arg.date, "%Y-%m-%d").timetuple().tm_yday, end="")


if __name__ == "__main__":
    main()
