import ctypes
import lzma

from pathlib import Path

import astropy.units as u  # pyright: ignore[reportMissingTypeStubs]
import numpy as np

from astropy.time import Time  # pyright: ignore[reportMissingTypeStubs]
from impisc.packets import TemperaturePacket  # pyright: ignore[reportMissingTypeStubs]

from . import progress_bar

type TemperatureSeries = dict[str, Time | u.Quantity]
SCIENCE_TEMPERATURES: list[str] = [
    "daqbox_ch1",
    "daqbox_ch2",
    "daqbox_ch3",
    "daqbox_ch4",
]
HOUSEKEEPING_TEMPERATURES: list[str] = [
    "eps_heater",
    "cm4_power_module",
    "bubba_amp",
    "instrument_heater",
    "fc_board_temperature",
]


def load_file(file: Path, which: list[str] | None = None) -> TemperatureSeries:
    """Read which temperatures from the provided temperature file.
    if which is not specified, it reads all temperatures.
    """
    times: list[int] = []
    temperatures: list[list[float]] = []
    if which is None:
        which = [f[0] for f in TemperaturePacket._fields_]
    with lzma.open(file, "rb") as f:
        while data := f.read(ctypes.sizeof(TemperaturePacket)):
            pkt = TemperaturePacket.from_buffer_copy(data)
            times.append(pkt.timestamp)
            temperatures.append([getattr(pkt, field) / 10 for field in which])

    return {
        "times": Time(times, format="unix"),
        "temperatures": (temperatures << u.deg_C),
    }


def _load_files(files: list[Path], which: list[str]) -> TemperatureSeries:
    """Helper for loading different sets of temperatures."""

    def temperature_bar(i: int, length: int):
        progress_bar.pprint(
            i, length, prefix="Loading temperature data:", suffix="Complete"
        )

    length = len(files)
    times, temperatures = [], []
    for i, file in enumerate(files):
        current: TemperatureSeries = load_file(file, which=which)
        times.append(current["times"])
        temperatures.append(current["temperatures"])
        temperature_bar(i + 1, length)

    return {
        "times": np.concatenate(times),
        "temperatures": np.vstack(temperatures),
    }


def load_science_temperatures(files: list[Path]) -> TemperatureSeries:
    """Read data from all files, filtered by science temperatures."""
    return _load_files(files, which=SCIENCE_TEMPERATURES)


def load_housekeeping_temperatures(files: list[Path]) -> TemperatureSeries:
    """Read data from all files, filtered by housekeeping temperatures."""
    return _load_files(files, which=HOUSEKEEPING_TEMPERATURES)
