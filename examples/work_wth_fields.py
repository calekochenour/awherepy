"""
Work with Fields in aWherePy
============================

Learn how to create, get, update, and delete fields with aWherePy.

"""

###############################################################################
# Create, Get, Update, and Delete Fields with aWherePy
# ----------------------------------------------------
#
# .. note::
#    The example below will show you how to use the ``create_field()``.
#    ``get_fields()``, ``update_field()``, and ``delete_field()`` functions to
#    to work with fields in the aWhere API.
#
# In this vignette, you will create an example field located in Manchester,
# Vermont. You will also get the field, update the field, and delete the field.
# aWhere API data can be accessed by inputting locations or fields (which
# also have locations) into the API calls. A field created with this workflow
# can be used with other aWherePy modules.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import awherepy.fields as awf

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
# Create an aWhere Field
# ----------------------
#
# To create a field within the aWhere API, a you must specify a field ID and
# location (longitude, latitude) associated with the field. You may also
# include a field name, farm ID, and area in acres, but this is not required
# for the funtion to work. You create an aWhere field with the
# ``create_field()`` function.

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

###############################################################################
# Get an aWhere Field
# -------------------
#
# Creating an aWhere field returs the field in geodataframe format when the
# field is created. However, once a field is created, another with with the
# same field ID cannot be created unless the original field is deleted first.
# When you want to access and store that field in a geodataframe after it has
# already been created, you used the ``get_fields()`` function. This function
# allows you to access a specific field (by field ID) or all fields within an
# aWhere application.

# Get all fields associated with an aWhere application
all_fields = awf.get_fields(awhere_api_key, awhere_api_secret)


# Get a single field, specified by field ID
single_field = awf.get_fields(
    awhere_api_key, awhere_api_secret, kwargs={"field_id": "VT-Manchester"}
)

###############################################################################
# Update an aWhere Field
# ----------------------
#
# There may be a time when you need to update some of the parameters in a
# field. This can be completed with the ``update_field()`` function. Note that
# at this time, the aWhere API only supports updates of the field name and farm
# id. The field ID is required input so that the aWhere API can update the
# correct field.

# Define update info
update_info = {
    "field_id": "VT-Manchester",
    "field_name": "VT-Manchester-Field-Update",
    "farm_id": "VT-Mancheseter-Farm-Update",
}

# Update field
field = awf.update_field(
    awhere_api_key, awhere_api_secret, field_info=update_info
)

###############################################################################
# Delete an aWhere Field
# ----------------------
#
# If you need to delete a field, you use the ``delete_field()`` function. This
# may be necessary if you want to re-use a field ID, as you cannot have more
# than one field with the same field ID. The field ID is used as the identifer
# to locate the field for deletion.

# Delete field
output_message = awf.delete_field(
    awhere_api_key, awhere_api_secret, field_id="VT-Manchester"
)
