"""
Convert raw science data into level 1.
"""

import argparse

from pathlib import Path

import asdf

from pipeline import file_grabbers, science, temperatures

LEVEL1_FILE_FORMAT = "impish-{year:04}-{doy:03}-{hour:02}-level1.asdf"


def write_asdf(
    temps_data: temperatures.TemperatureSeries,
    science_data: science.ScienceSeries,
    file_name: str,
    compression: str,
):
    """Write the level 1 data to an ASDF file."""
    tree = {
        "temperatures": temps_data,
        "science": science_data
    }
    af = asdf.AsdfFile(tree=tree)
    af.write_to(fd=file_name, all_array_compression=compression)
    af.close()


def main():

    parser = argparse.ArgumentParser(
        description="Process level0 data into level1.",
        epilog="Example of use: python level1.py 2026 176 ./science ./temperature",
    )
    _ = parser.add_argument("year", type=int)
    _ = parser.add_argument("doy", help="UTC day of year", type=int)
    _ = parser.add_argument(
        "science_dir", help="directory with the science files", type=str
    )
    _ = parser.add_argument(
        "temperature_dir", help="directory with the temperature files", type=str
    )
    _ = parser.add_argument(
        "-c",
        "--compression",
        default="zlib",
        help="compression for the asdf file, passed to asdf.AsdfFile.writeto",
        type=str,
        required=False,
    )
    arg = parser.parse_args()
    year: int = arg.year
    doy: int = arg.doy
    ranges = ((0, 6), (6, 12), (12, 18), (18, 24))
    for hour_range in ranges:
        temperature_files: list[Path] = []
        science_files: list[Path] = []
        for hour in range(*hour_range):
            try:
                temperature_files += file_grabbers.get_temperature_files(
                    year, doy, hour, directory=Path(arg.temperature_dir)
                )
                science_files += file_grabbers.get_science_files(
                    year, doy, hour, Path(arg.science_dir)
                )
            except ValueError:
                break
        if len(temperature_files) == 0:
            continue
        science_temps: temperatures.TemperatureSeries = (
            temperatures.load_science_temperatures(temperature_files)
        )
        # housekeeping_temps: temperatures.TemperatureSeries = temperatures.load_housekeeping_temperatures(temperature_files)
        science_data: science.ScienceSeries = science.load_science_data(science_files)

        outfile: str = LEVEL1_FILE_FORMAT.format(year=year, doy=doy, hour=hour_range[0])
        write_asdf(science_temps, science_data, outfile, arg.compression)
        print(f"wrote level 1 file: {outfile}\n")


if __name__ == "__main__":
    main()
