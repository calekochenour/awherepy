Get Started With aWherePy
=========================

aWherePy is a python package built to retrieve, extract, and format weather and agronomic data from the aWhere API.

aWherePy Module and Function Documentation
------------------------------------------

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

Dependencies
~~~~~~~~~~~~

aWherePy has several Python package dependencies. The easiest way to install aWherePy is to use the awhere-python conda environment: LINK TO ENVIRONMENT GITHUB HERE. This will ensure that you have all of the required dependencies needed to run aWherePy.

Alternatively, use pip to install aWherePy. ``--upgrade`` is optional but it ensures that the package overwrites when you install and you have the current version. If you don't have the package yet you can still use the ``--upgrade`` argument.

``pip install awherepy``

Once aWherePy is installed you can import it into Python.

    >>> import awherepy as awp

You can also import the individual modules as follows:

    >>> import awherepy.agronomics as aa
    >>> import awherepy.crops as ac
    >>> import awherepy.fields as af
    >>> import awherepy.grid as ag
    >>> import awherepy.models as am
    >>> import awherepy.plantings as ap
    >>> import awherepy.weather as aw

Data
~~~~

Example data to work with aWherePy can be bound here: LINK TO EXAMPLE DATA
