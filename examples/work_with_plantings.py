"""
Work with Plantings in aWherePy
===============================

Learn how to create, get, and delete plantings with aWherePy.

"""

###############################################################################
# Create, Get, and Delete Plantings with aWherePy
# -----------------------------------------------
#
# .. note::
#    The example below will show you how to use the ``create_planting()``,
#    ``get_plantings()``, and ``delete_plantings()`` functions to work with
#    fields in the aWhere API.
#
# In this vignette, you will create an example field located in Manchester,
# Vermont and add a planting (crop) to the field. You will also get the
# planting, delete the planting.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import awherepy.fields as awf
import awherepy.plantings as awp

###############################################################################
# Prerequisites
# -------------
#
# In order to make calls to any aWhere API, you must provide a valid API key
# and secret. The key and secret used in this example are stored as
# environment variables.

# Define aWhere API key and secret
awhere_api_key = os.environ.get("AWHERE_API_KEY")
awhere_api_secret = os.environ.get("AWHERE_API_SECRET")

###############################################################################
# Create an aWhere Planting
# -------------------------
#
# To create a planting within the aWhere API, you must first create an aWhere
# field and then add the planting to that field. You can create a field with
# ``create_field()`` function from the ``awherepy.crops`` module, and you can
# then add a planting to that field with the ``create_planting()`` function.

# Define field paramaters
field_info = {
    "field_id": "VT-Manchester",
    "field_name": "VT-Manchester-Field",
    "farm_id": "VT-Manchester-Farm",
    "center_latitude": 43.1636875,
    "center_longitude": -73.0723269,
    "acres": 10,
}

# Create field
try:
    field = awf.create_field(
        awhere_api_key, awhere_api_secret, field_info=field_info
    )

# Delete field if already exists
except KeyError:
    awf.delete_field(
        awhere_api_key, awhere_api_secret, field_id=field_info.get("field_id"),
    )

    # Create field again
    field = awf.create_field(
        awhere_api_key, awhere_api_secret, field_info=field_info
    )

# Define planting parameters
planting_info = {
    "crop": "wheat-hardred",
    "planting_date": "2020-05-01",
    "projected_harvest_date": "2020-09-30",
    "projected_yield_amount": 200,
    "projected_yield_units": "boxes",
}

# Create planting
planting = awp.create_planting(
    awhere_api_key,
    awhere_api_secret,
    field_id="VT-Manchester",
    planting_info=planting_info,
)

###############################################################################
# Get an aWhere Planting
# ----------------------
#
# Creating an aWhere field returns the planting in dataframe format when the
# planting is created. In order to retrieve the planting after it has been
# created, you can use the ``get_plantings()`` function with a specific field
# ID and planting ID as input parameters. An alternative method to retrieve
# the planting is to retrieve the current planting by including this in the
# parameters instead of providing a specific field ID and planting ID. Note
# that this will retrieve the most recent planting in any field and will only
# return the planting created above if no other plantings have been created
# since.

# Get planting
planting = awp.get_plantings(
    awhere_api_key, awhere_api_secret, kwargs={"planting_id": "current"}
)

###############################################################################
# Delete an aWhere Planting
# -------------------------
#
# If you need to delete a planting, you use the ``delete_planting()``
# function. If you want to delete a field other than the most recent, you must
# specify the planting ID in the function parameters. Otherwise, the
# current planting will be deleted. Also note that all plantings associated
# with a specific field will be deleted when you delete that field.

# Delete planting
output_message = awp.delete_planting(
    awhere_api_key, awhere_api_secret, field_id="VT-Test"
)
