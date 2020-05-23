[![Build Status](https://travis-ci.org/calekochenour/awherepy.svg?branch=master)](https://travis-ci.org/calekochenour/awherepy)
[![Build status](https://ci.appveyor.com/api/projects/status/donws1p4r2w4wcy1?svg=true)](https://ci.appveyor.com/project/calekochenour/awherepy)
[![codecov](https://codecov.io/gh/calekochenour/awherepy/branch/master/graph/badge.svg)](https://codecov.io/gh/calekochenour/awherepy)
[![Documentation Status](https://readthedocs.org/projects/awherepy/badge/?version=latest)](https://awherepy.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/calekochenour/awherepy/shield.svg)](https://pyup.io/repos/github/calekochenour/awherepy/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

# aWherePy

## Why aWherePy?

aWhere's agronomic and weather data API is currently accessible through the R programming language. aWherePy creates a Python solution for the aWhere API and provides Python code to:

* Connect to the aWhere API;
* Get data from the aWhere API;
* Extract data from the aWhere API returns;
* Clean and georeference extracted data;
* Create an aWhere-sized (9 km x 9 km) grid from a shapefile; and,
* Rasterize existing remote sensing and GIS data to the aWhere grid.

aWherPy allows for the creation of reproducible science workflows with Python scripts and/or Jupyter Notebooks.  

## View Example aWherePy Applications

## Install aWherePy
<!--
aWherePy can be installed using `pip`, but we **strongly** recommend that you install it using conda and the `conda-forge` channel.

### Install Using Conda / conda-forge Channel (Preferred)

If you are working within an Anaconda environment, we suggest that you install EarthPy using
`conda-forge`

```bash
$ conda install -c conda-forge awherepy
```

Note: if you want to set conda-forge as your default conda channel, you can use the following install workflow.

We recommmend this approach. Once you have run conda config, you can install awherepy without specifying a channel.

```bash
$ conda config --add channels conda-forge
$ conda install awherepy
```

### Install via Pip

We strongly suggest that you install aWherePy using conda-forge given pip can be more prone to  spatial library dependency conflicts. However, you can install earthpy using pip.

To install aWherePy via `pip` use:

```bash
$ pip install --upgrade awherepy
```

Once you have successfully installed awherepy, you can import it into Python.

```python
>>> import awherepy as ap
```
-->

## Active Maintainers

Contributions to aWherePy are welcome. Below are the current active package maintainers. Please see the
[contributors file](https://awherepy.readthedocs.io/en/latest/contributors.html) for a complete list of all of maintainers.

<a title="Cale Kochenour" href="https://www.github.com/calekochenour"><img width="60" height="60" alt="Cale Kochenour" class="pull-left" src="https://user-images.githubusercontent.com/54423680/82125272-10a41780-9762-11ea-9026-f705caa25e8e.PNG?size=120" /></a>

## How to Contribute

Contributions to aWherePy are welcome. Please see the
[contributing guidelines](https://awherepy.readthedocs.io/en/latest/contributing.html) for more information about submitting pull requests or changes to aWherePy.

## License

[BSD-3](https://github.com/calekochenour/awherepy/blob/master/LICENSE)

<!--
## 1. Prerequisites

To run this analysis locally or online with Binder, you will need:

 * [aWhere Developer Account](https://developer.awhere.com/)

If running this locally, you will also need:

 * Conda ([Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://docs.anaconda.com/anaconda/install/))

## 2. Binder Setup Instructions
To run this analysis in a web browser, click the icon below to launch the project with Binder:

[![Binder](https://mybinder.org/badge_logo.svg)]()

## 3. Local Setup Instructions

To run this analysis from a terminal, navigate to the folder containing the local repository.

Local instructions assume the user has cloned or forked the GitHub repository.

### Create and Activate Conda Environment

From the terminal, you can create and activate the project Conda environment.

Create environment:

```bash
conda env create -f environment.yml
```

Activate environment:

```bash
conda activate INSERT ENVIRONMENT NAME
```

### Open Jupyter Notebook

From the terminal, you can run the analysis and produce the project outputs.

Open Jupyter Notebook:

```bash
jupyter notebook
```

## 4. Run the Analysis

Follow these steps upon completion of the **Binder Setup Instructions** or **Local Setup Instructions** to run the analysis in Jupyter Notebook:

* Navigate to the INSERT FOLDER NAME HERE folder;

* Click on the INSERT JUPYTER NOTEBOOK FILE NAME HERE file;

## 5. Demos

### Run Analysis

### View Results

## 6. Contents

The project contains folders for all stages of the workflow as well as other files necessary to run the analysis.

### `01-code-scripts/`

Contains all Python scripts and Jupyter Notebooks required to run the analysis.

### `02-raw-data/`

Contains all original/unprocessed data.

### `03-processed-data/`

Contains all processed/created data.

### `04-graphics-outputs/`

Contains all figures.

### `05-papers-writings/`

Contains all paper/report files.

### `Makefile`

Contains instructions to execute the code.

### `environment.yml`

Contains the information required to create the Conda environment.
-->
