# `pipeline`
---
Processing pipeline for IMPISH data.
Everything is currently subject to change as things develop.


# Installation
---

## `uv`
```
git clone https://github.com/umn-impish/pipeline.git
cd pipeline
./INSTALL
```

## other
```
git clone https://github.com/umn-impish/pipeline.git
cd pipeline
# any virtual env steps
pip install .
```

# Description
---

There are some handy tools included in the installation:
- `getdoy` converts a `YYYY-MM-DD` date into a day-of-year
- `lvl1` converts level 0 data into level 1 data


# Rough outline of data levels
---
| Level 0              | Level 1                     | Level 2                              |
|----------------------|-----------------------------|--------------------------------------|
| Raw data from IMPISH | Intermittent data product   | Science-ready data                   |
| Many small files     | One file per day            | Applied detector calibration         |
|                      | Spectra grouped with T data | Adjusted for IMPISH lat/lon/altitude |
