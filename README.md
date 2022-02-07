# naaf

`naaf` is a library for reading and writing Cryo-ET data.

# Installation

```
pip install naaf
```


# Usage

This command will land in an ipython shell with the loaded data collected in a list called `data`:

```bash
naaf path/to/files/ /other/path/to/file.star
```


# Features

Currently `naaf` is capable of reading images in the following formats:
- `.mrc`
- Dynamo `.em`

and particle data in the following formats:
- Relion `.star`
- Dynamo `.tbl`
- Cryolo `.cbox` and `.box`

# Data structures

Data is loaded into simple data objects called `Particles` or `Image`. They have the following attributes:

```python
Data.name  # name guessed from the data or file path
Data.source  # path to the file containing this data
Data.pixel_size  # pixel size information extracted from the data. None if absent.

Particles.data  # pandas DataFrame with coordinates, rotations and arbitary particle features

Image.data  # data array with pixel intensities
```

## Particle orientations

Orientations are `scipy` `Rotation` objects. They can be handled normally in a pandas dataframe. They also provide useful batch tools:

- `Rotation.concatenate(array_of_rotations)` will merge all the rotation objects into one
- `rotation_object.apply(vectors)` will apply the rotation(s) (following numpy broadcasting rules) to vector(s)

## Image data

When possible (and unless disabled), naaf loads images lazily using `dask`. The resulting objects can be treated as normal numpy array, except one needs to call `array.compute()` to apply any pending operations and return the result.
