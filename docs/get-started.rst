Get Started With aWherePy
=========================

aWherePy is a python package built to retrieve, extract, and format weather and agronomic data from the aWhere API.

aWherePy Modules
----------------

All functions are included in the 7 awherepy modules:

- agronomics
- crops
- fields
- grid
- models
- plantings
- weather

Install aWherePy
----------------

The recommended method to install aWherePy for use and testing is to install it within an Anaconda environment using the ``conda-forge`` channel.

Note: Installing aWherePy with ``pip`` will fail due to incompatibilities with ``pip`` and the ``rtree`` package (specifically ``rtree>=0.9.0``), which is required for aWherePy functionality.

Install Conda
~~~~~~~~~~~~~

You must install Conda - `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ (recommended) or `Anaconda <https://docs.anaconda.com/anaconda/install/>`_ - in order to create a Conda environment and install aWherePy with `conda-forge`.

Install aWherePy within Conda Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Within an active Conda environment, install aWherePy::

    $ conda install -c conda-forge awherepy

Use aWherePy within Terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once installed, can import aWherePy into Python:

    >>> import awherepy as aw

You can also import the individual modules into Python:

    >>> import awherepy.agronomics as awa
    >>> import awherepy.crops as awc
    >>> import awherepy.fields as awf
    >>> import awherepy.grid as awg
    >>> import awherepy.models as awm
    >>> import awherepy.plantings as awp
    >>> import awherepy.weather as aww

Test aWherePy
~~~~~~~~~~~~~

The root directory of aWherePy contains the ``requirements-dev.txt`` file, which provides all package dependencies for testing aWherePy.

Within the active Conda environment that contains aWherePy, install the test dependencies::

    $ pip install -r requirements-dev.txt

One the testing dependencies are installed, run the complete aWherePy test suite::

    $ pytest

Before running ``pytest``, make sure that you are in the root aWherePy folder. You must also have the datasets located in ``awherepy/example-data`` and the test scripts located in ``awherepy/tests``.

Note: In order to work with aWherePy, you must possess a valid API key and API secret (associated with an active `aWhere account <https://apps.awhere.com/>`_). All modules (with the exception of grids) requires the API key and API secret to authenticate prior to making any API requests. Otherwise, the functions within the modules will raise errors indicating invalid credentials.
