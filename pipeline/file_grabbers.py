"""
Simple functions for obtaining science and temperature files.
"""

from pathlib import Path

TEMPERATURE_PREFIX: str = "impish_temperatures_{year:04}-{doy:03}-{hour:02}"
SCIENCE_PREFIX: str = "science_{year:04}-{doy:03}-{hour:02}"


def _get_files(directory: Path, glob: str) -> list[Path]:
    """Get files from the directory matching the provided glob."""
    if not directory.exists():
        raise ValueError(f"Provided input directory does not exist: {directory}")
    files = sorted(list(directory.glob(glob)))
    print(f"file search in {directory.resolve()}:\n\tglob: {glob}")
    print(f"\tfound {len(files)} files")
    if not files:
        raise ValueError(f"No matching files found in directory")
    print(f"first file: {files[0]}\nlast file:  {files[-1]}")

    return files


def get_science_files(year: int, doy: int, hour: int, directory: Path) -> list[Path]:
    """Get all science files from the specified day."""
    return _get_files(
        directory=directory,
        glob=f"{SCIENCE_PREFIX.format(year=year, doy=doy, hour=hour)}*.bin.bz2",
    )


def get_temperature_files(year: int, doy: int, hour: int, directory: Path) -> list[Path]:
    """Get all temperature files from the specified day."""
    return _get_files(
        directory=directory,
        glob=f"{TEMPERATURE_PREFIX.format(year=year, doy=doy, hour=hour)}*.bin.xz",
    )
