import bz2
import multiprocessing as mp

from pathlib import Path

import astropy.units as u  # pyright: ignore[reportMissingTypeStubs]
import numpy as np

from astropy.time import Time  # pyright: ignore[reportMissingTypeStubs]

from . import progress_bar

type ScienceSeries = dict[str, Time | u.Quantity | np.ndarray]


# The number of science bins lives in `/data/config/variables.env`
# onboard IMPISH
NUM_BINS = 1000
NUM_DAQBOX_CHANNELS = 4


def load_file(file: Path) -> ScienceSeries:
    """Loads data from a single science file."""
    with bz2.open(file, "rb") as f:
        raw_data = f.read()
    record_dtype = np.dtype(
        [
            ("timestamp", "<u4"),
            ("frame", "u1"),
            ("spectra", "<u4", (NUM_DAQBOX_CHANNELS, NUM_BINS)),
        ]
    )
    records = np.frombuffer(raw_data, dtype=record_dtype)
    dt = 1 / 32
    midpoints = records["timestamp"] + (records["frame"] / 32.0) + (dt / 2.0)
    counts = records["spectra"].astype(np.uint16)

    return {
        "time_mids": Time(midpoints, format="unix"),
        "time_deltas": (dt << u.s).to(u.ms) * np.ones_like(midpoints),
        "counts": counts,
    }


def load_science_data(files: list[Path]) -> ScienceSeries:
    """Loads all science data. The reading is parallelized."""

    def science_bar(i: int, length: int):
        progress_bar.pprint(
            i, length, prefix="Loading science data:", suffix="Complete"
        )
    length = len(files)
    pool = mp.Pool(processes=mp.cpu_count())
    mids, deltas, counts = [], [], []
    for (mid, delta, count) in pool.imap(_load_science_data_helper, files, chunksize=20):
        mids.append(mid[0])
        deltas.append(delta[0])
        counts.append(count[0])
        science_bar(len(mids), length)

    # Combine without storing a duplicate in RAM
    total_len = sum(arr.shape[0] for arr in counts)
    out = np.empty((total_len, *counts[0].shape[1:]), dtype=counts[0].dtype)
    idx = total_len
    while counts:
        arr = counts.pop()
        idx -= arr.shape[0]
        out[idx : idx + arr.shape[0]] = arr

    return {
        "time_mids": Time(mids),
        "time_deltas": np.concatenate(deltas),
        "counts": out * u.ct,
    }


def _load_science_data_helper(
    *files: Path,
) -> tuple[list]:
    """Helper for parallelized science data loading."""
    mids, deltas, counts = [], [], []
    for file in files:
        current = load_file(file)
        mids.append(current["time_mids"])
        deltas.append(current["time_deltas"])
        counts.append(current["counts"])

    return (mids, deltas, counts)
