import argparse

from pathlib import Path

import asdf

from pipeline import file_grabbers, science, temperatures

LEVEL1_FILE_FORMAT = "impish-{year:04}-{doy:03}-level1.asdf"


def write_asdf(
    temps_data: temperatures.TemperatureSeries,
    science_data: science.ScienceSeries,
    file_name: str,
    compression: str,
):

    tree = {"temperatures": temps_data, "science": science_data}
    af = asdf.AsdfFile(tree=tree)
    af.write_to(fd=file_name, all_array_compression=compression)


def main():

    parser = argparse.ArgumentParser(
        description="Process level0 data into level1.",
        epilog="Example of use: python level1.py 2026 176 ./science ./temperature",
    )
    _ = parser.add_argument("year", type=int)
    _ = parser.add_argument("doy", help="day of year", type=int)
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
        help="compression for the asdf file",
        type=str,
        required=False,
    )
    arg = parser.parse_args()

    year: int = arg.year
    doy: int = arg.doy
    temperature_files: list[Path] = file_grabbers.get_temperature_files(
        year, doy, Path(arg.temperature_dir)
    )
    science_temps: temperatures.TemperatureSeries = (
        temperatures.load_science_temperatures(temperature_files)
    )
    # housekeeping_temps: temperatures.TemperatureSeries = temperatures.load_housekeeping_temperatures(temperature_files)

    science_files: list[Path] = file_grabbers.get_science_files(
        year, doy, Path(arg.science_dir)
    )
    science_data: science.ScienceSeries = science.load_science_data(science_files)

    outfile: str = LEVEL1_FILE_FORMAT.format(year=year, doy=doy)
    write_asdf(science_temps, science_data, outfile, arg.compression)
    print(f"wrote level 1 file: {outfile}")


if __name__ == "__main__":
    main()
