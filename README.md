[![Build Status](https://travis-ci.org/calekochenour/awherepy.svg?branch=master)](https://travis-ci.org/calekochenour/awherepy)
[![Build status](https://ci.appveyor.com/api/projects/status/donws1p4r2w4wcy1?svg=true)](https://ci.appveyor.com/project/calekochenour/awherepy)
[![codecov](https://codecov.io/gh/calekochenour/awherepy/branch/master/graph/badge.svg)](https://codecov.io/gh/calekochenour/awherepy)
[![Documentation Status](https://readthedocs.org/projects/awherepy/badge/?version=latest)](https://awherepy.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

# aWherePy

aWherePy provides a Python solution to work with the [aWhere API](https://www.awhere.com/developer/).

## Why aWherePy?

Prior to aWherePy, aWhere's agronomic and weather data API was only accessible with R. aWherePy creates a Python solution for the aWhere API and provides Python code to:

* Call the aWhere API;
* Extract data from the aWhere API returns;
* Clean and georeference extracted data;
* Track crops and agricultural data over time;
* Create an aWhere-sized (9 km x 9 km) grid from a shapefile; and,
* Rasterize existing remote sensing and GIS data to the aWhere grid.

aWherePy allows for the creation of reproducible science workflows with Python scripts and/or Jupyter Notebooks and creates the vehicle to integrate aWhere data with other geospatial and remote sensing data within these platforms.

aWherePy contains seven modules:

* agronomics;
* crops;
* fields;
* grids;
* models:
* plantings; and,
* weather.

aWherePy [weather](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_weather.html#sphx-glr-gallery-vignettes-work-with-weather-py) and [agronomics](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_agronomics.html#sphx-glr-gallery-vignettes-work-with-agronomics-py) modules provide the functionality to get historical norms, observed values, and forecast values for weather and agriculture metrics that are formatted, georeferenced, and ready for data analysis and visualization.

aWherePy [grids](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_grids.html#sphx-glr-gallery-vignettes-work-with-grids-py) module provides functionality to rasterize data to the aWhere grid (9x9 km cells). This allows you to integrate other geospatial and remote sensing data (e.g. world population data, normalized difference vegetation index data) with aWhere API data to create advanced analytical insights.

aWherePy [fields](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_fields.html#sphx-glr-gallery-vignettes-work-with-fields-py), [crops](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_crops.html#sphx-glr-gallery-vignettes-work-with-crops-py), [plantings](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_plantings.html#sphx-glr-gallery-vignettes-work-with-plantings-py), and [models](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/work_with_models.html#sphx-glr-gallery-vignettes-work-with-models-py) modules provide access to advanced agricultural models that track crop data over time and produce information that allows you to make real-time agricultural decisions and adjustments.

## aWherePy Package Structure

aWherePy reflects the currently capabilities of the aWhere API. This section outlines the structure of the aWherePy package, as it relates to the seven package modules.

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


## View Example aWherePy Applications

You can view aWherePy applications in the [vignette gallery](https://awherepy.readthedocs.io/en/latest/gallery_vignettes/index.html), which demonstrates functionality for all seven aWherePy modules.

In addition, the aWherePy package contains [Python scripts](https://github.com/calekochenour/awherepy/tree/master/examples) to run the example applications for each module as well as the [example data](https://github.com/calekochenour/awherepy/tree/master/awherepy/example-data) used within the Python scripts.

## Install aWherePy

Installing aWherePy 0.1.0 directly from GitHub with pip will fail due to incompatibilities with pip and the `rtree` package (specifically `rtree>=0.9.0`), which is required for aWherePy functionality.

The recommended method to install aWherePy 0.1.0 for local testing and evaluation is to fork or clone the repository, install Conda, create a Conda environment with the necessary packages, and run the complete test suite.

### Fork or Clone aWherePy

Once you have forked aWherePy or copied the aWherePy clone link, you can run the following terminal command within a local directory to initialize the repository.

If fork:
```bash
$ git clone https://github.com/YOUR-USERNAME/awherepy.git
```

If clone:
```bash
$ git clone https://github.com/calekochenour/awherepy.git
```

### Install Conda

You must install Conda - [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (recommended) or [Anaconda](https://docs.anaconda.com/anaconda/install/) - in order to create a Conda environment that will run the complete aWherePy test suite.

### Create aWherePy Development Conda Environment

The root directory of aWherePy contains the `environment-dev.yml` file, which when used to create a Conda environment, provides all packages (functionality and testing) to run the complete aWherePy test suite.

From the terminal, you can create the development Conda environment.

Create environment:

```bash
$ conda env create -f environment-dev.yml
```

### Activate Conda Environment and Run aWherePy Test Suite

Once the aWherePy development environment is created, you can activate it and run the complete test suite.

Activate environment:

```bash
$ conda activate awherepy-dev
```

Run test suite:

```bash
$ pytest
```

Note: Before running `pytest`, make sure that you are in the root aWherePy folder.

### Use aWherePy within Terminal

Once installed with a fork or clone, you can also use aWherePy for reasons other than testing. For example, you can import aWherePy into Python:

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

## aWhere API Authentication

In order to work with aWherePy, you must possess a valid API key and API secret (associated an active [aWhere account](https://apps.awhere.com/)). All modules (with the exception of grids) requires the API key and API secret to authenticate prior to making any API requests. Otherwise, the functions within the modules will raise errors indicating invalid credentials.

The credentials used in all examples, tests, and documentation are stored and shown as environment variables in the following way:

```python
>>> # Define aWhere API key and secret
>>> awhere_api_key = os.environ.get("AWHERE_API_KEY")
>>> awhere_api_secret = os.environ.get("AWHERE_API_SECRET")
```

For both aWherePy continuous integration builds ([Travis CI](https://travis-ci.org/github/calekochenour/awherepy), [AppVeyor](https://ci.appveyor.com/project/calekochenour/awherepy)), the API key and secret are stored as secure environment variables, which allows the full suite of tests to run and the code coverage to be updated upon completion of the build.

The aWhere API credentials are not transferable and will not be downloaded when you install, fork, or clone aWherePy. Because of this, all tests (with the exception of the grids module) will fail when run locally, unless you have a valid aWhere API key and API secret. Note that credentials can be stored in different ways locally (e.g. environment variables, text file, other means), but tests may have to be altered to fit a method other than environment variables, as shown in the examples, tests, and documentation.

## Example Usage

This example shows how to get weather data for a single aWhere grid cell near Rocky Mountain National Park (RMNP), Colorado, using the aWherePy grids and weather modules.

```python
>>> # Imports
>>> import os
>>> import awherepy.grids as awg
>>> import awherepy.weather as aww

>>> # Define aWhere API key and secret
>>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
>>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')

>>> # Define path to RMNP boundary
>>> rmnp_bound_path = os.path.join(
...     "..", "awherepy", "example-data", "colorado_rmnp_boundary.shp"
... )   

>>> # Create aWhere grid and EPSG 4326 boundary for RMNP
>>> rmnp_grid, rmnp_bound_4326 = awg.create_grid(rmnp_bound_path,
...    buffer_distance=0.12
... )

>>> # Extract RMNP grid centroids to list
>>> rmnp_grid_centroids = awg.extract_centroids(rmnp_grid)

>>> # Get first centroid
>>> analysis_centroid = rmnp_grid_centroids[0]

>>> # Define RMNP norms kwargs
>>> rmnp_weather_norms_kwargs = {
...     "location": (analysis_centroid[0], analysis_centroid[1]),
...     "start_date": "05-04",
...     "end_date": "05-13",
... }

>>> # Get RMNP weather norms, 05-04 to 05-13
>>> rmnp_weather_norms = aww.get_weather_norms(
...     awhere_api_key, awhere_api_secret, kwargs=rmnp_weather_norms_kwargs
... )

>>> # Get precipitation average from weather norms data
>>> rmnp_precip_norms = rmnp_weather_norms[["precip_avg_mm"]]

>>> # Define RMNP observed weather kwargs
>>> rmnp_weather_observed_kwargs = {
...     "location": (analysis_centroid[0], analysis_centroid[1]),
...     "start_date": "2014-05-04",
...     "end_date": "2014-05-13",
... }

>>> # Get observed weather
>>> rmnp_weather_observed = aww.get_weather_observed(
...     awhere_api_key, awhere_api_secret, kwargs=rmnp_weather_observed_kwargs
... )

>>> # Get precipitation amount from observed weather data
>>> rmnp_precip_observed = rmnp_weather_observed[["precip_amount_mm"]]
```

## aWherePy Documentation

For information about how to use aWherePy modules and functions, see example applications, and view all other aWherePy documentation-related material, review the [aWherePy documentation](https://awherepy.readthedocs.io/en/latest/).

## Related Packages

There are no existing Python packages that provide similar functionality for the aWhere API, which is the primary reason aWherePy was created. aWherePy is based on the [aWhere R Library](https://github.com/aWhereAPI/aWhere-R-Library), which is an R package created by aWhere for use with the aWhere API.

## Active Maintainers

Contributions to aWherePy are welcome. Below are the current active package maintainers. Please see the
[contributors page](https://awherepy.readthedocs.io/en/latest/contributors.html) for a complete list of all of maintainers.

<a title="Cale Kochenour" href="https://www.github.com/calekochenour"><img width="60" height="60" alt="Cale Kochenour" class="pull-left" src="https://user-images.githubusercontent.com/54423680/82125272-10a41780-9762-11ea-9026-f705caa25e8e.PNG?size=120" /></a>

## How to Contribute

Contributions to aWherePy are welcome. Please see the
[contributing guidelines](https://awherepy.readthedocs.io/en/latest/contributing.html) for more information about submitting pull requests or changes to aWherePy.

## License

[BSD-3](https://github.com/calekochenour/awherepy/blob/master/LICENSE)
