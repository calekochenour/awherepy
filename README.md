[![Build Status](https://travis-ci.org/calekochenour/awherepy.svg?branch=master)](https://travis-ci.org/calekochenour/awherepy)
[![Build status](https://ci.appveyor.com/api/projects/status/donws1p4r2w4wcy1?svg=true)](https://ci.appveyor.com/project/calekochenour/awherepy)
[![codecov](https://codecov.io/gh/calekochenour/awherepy/branch/master/graph/badge.svg)](https://codecov.io/gh/calekochenour/awherepy)
[![Documentation Status](https://readthedocs.org/projects/awherepy/badge/?version=latest)](https://awherepy.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# aWherePy

aWherePy provides a Python solution to work with the [aWhere API](https://www.awhere.com/developer/).

## Why aWherePy?

Prior to aWherePy, aWhere's agronomic and weather data API was only accessible with [R](https://github.com/aWhereAPI/aWhere-R-Library). aWherePy creates a Python solution for the aWhere API and provides Python code to:

* Call the aWhere API;
* Extract data from the aWhere API returns;
* Clean and georeference extracted data;
* Create an aWhere-sized (9 km x 9 km) grid from a shapefile; and,
* Rasterize existing remote sensing and GIS data to the aWhere grid.

aWherPy allows for the creation of reproducible science workflows with Python scripts and/or Jupyter Notebooks and creates the vehicle to integrate aWhere data and other geospatial and remote sensing data within these platforms.

## View Example aWherePy Applications

You can view aWherePy applications in the [vignette gallery](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/index.html), which demonstrates functionality for all seven aWherePy modules.

In addition, the aWherePy package contains [Python scripts](https://github.com/calekochenour/awherepy/tree/master/examples) to run the example applications for each module as well as the [example data](https://github.com/calekochenour/awherepy/tree/master/awherepy/example-data) used within the Python scripts.

## Install aWherePy

To install aWherePy from GitHub, run the following command in a terminal:

```bash
pip install git+https://github.com/calekochenour/awherepy.git#egg=awherepy
```

Once installed, you can import aWherePy into Python:

```python
>>> import awherepy as aw
```

You can also import the individual modules into Python:

```python
>>> import awherepy.agronomics as awa
>>> import awherepy.crops as awc
>>> import awherepy.fields as awf
>>> import awherepy.grid as awg
>>> import awherepy.models as awm
>>> import awherepy.plantings as awp
>>> import awherepy.weather as aww
```

## aWherePy Package Structure

aWherePy contains seven modules:

* agronomics;
* crops;
* fields;
* grids;
* models:
* plantings; and,
* weather.

This section outlines the structure of the aWherePy package, as it relates to these modules.

### `awherepy/`

Contains Python scripts for the aWherePy modules (e.g. `agronomics.py`). Also contains two sub-folders, one with example data and one with module test scripts.

### `awherepy/example-data`

Contains datasets used in the aWherePy tests and vignette gallery examples.

### `awherepy/tests`

Contains Python scripts for the aWherePy tests (e.g. `test_agronomics.py`).

### `docs/`

Contains files used to organize and populate the aWherePy documentation.

### `examples/`

Contains Python scripts used to in the aWherePy vignette gallery (e.g. `work_with_agronomics.py`).

## aWherePy Documentation

For information about how to use aWherePy modules and functions, see example applications, and view all other aWherePy documentation-related material, review the [aWherePy documentation](https://awherepy.readthedocs.io/en/latest/).

## Active Maintainers

Contributions to aWherePy are welcome. Below are the current active package maintainers. Please see the
[contributors file](https://awherepy.readthedocs.io/en/latest/contributors.html) for a complete list of all of maintainers.

<a title="Cale Kochenour" href="https://www.github.com/calekochenour"><img width="60" height="60" alt="Cale Kochenour" class="pull-left" src="https://user-images.githubusercontent.com/54423680/82125272-10a41780-9762-11ea-9026-f705caa25e8e.PNG?size=120" /></a>

## How to Contribute

Contributions to aWherePy are welcome. Please see the
[contributing guidelines](https://awherepy.readthedocs.io/en/latest/contributing.html) for more information about submitting pull requests or changes to aWherePy.

## License

[BSD-3](https://github.com/calekochenour/awherepy/blob/master/LICENSE)
