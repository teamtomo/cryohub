# cryohub

`cryohub` is a library for reading and writing Cryo-ET data based on the [`cryotypes`](https://github.com/teamtomo/cryotypes/) specification.

# Installation

```
pip install cryohub
```

# Usage

`cryohub` provides granular I/O functions such as `read_star` and `read_mrc`, which will all return objects following the `cryotypes` specification. A higher level function called `read` adds some magic to the IO procedure, guessing file formats and returning a list of `cryotypes`.

Similarly to the `read_*` functions, `cryohub` provides a series of `write_*` functions.


## From the command line

If you just need to quickly inspect your data, this command will land in an ipython shell with the loaded data collected in a list called `data`:

```bash
cryohub path/to/files/* /other/path/to/file.star
```


# Features

Currently `cryohub` is capable of reading images in the following formats:
- `.mrc` (and the `.mrcs` or `.st` variants)
- Dynamo `.em`
- EMAN2 `.hdf`

and particle data in the following formats:
- Relion `.star`
- Dynamo `.tbl`
- Cryolo `.cbox` and `.box`

Writer functions currently exist for:
- `.mrc`
- EMAN2 `.hdf`
- Dynamo `.em`
- Relion `.star`
- Dynamo `.tbl`

## Image data

When possible (and unless disabled), cryohub loads images lazily using [`dask`](https://docs.dask.org/en/stable/array.html). The resulting objects can be treated as normal numpy array, except one needs to call `array.compute()` to apply any pending operations and return the result.

# Contributing

Contributions are more than welcome! If there is a file format that you wish were supported in reading or writing, simply open an issue about it pointing to the specification. Alternatively, feel free to open a PR with your proposed implementation; you can look at the existing functions for inspiration.
