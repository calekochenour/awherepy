"""
Work with Agronomic Models in aWherePy
======================================

Learn how to get models, model details, and model results with aWherePy.

"""

###############################################################################
# Get Models, Model Details, and Model Results with aWherePy
# ----------------------------------------------------------
#
# .. note::
#    The example below will show you how to use the ``get_models()``,
#    ``get_model_details()``, and ``get_model_results()`` functions to work
#    to work with agronomic models in the aWhere API.
#
# In this vignette, you will get a list of available agronomic models in the
# aWhere API and get details about those models. Then, you will create an
# example field in Manchester, Vermont, add a hard red wheat crop to that field
# and get the model results for that crop.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import random
import awherepy.fields as awf
import awherepy.plantings as awp
import awherepy.models as awm

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
# Get All Models
# --------------
#
# To get a dataframe with all available aWhere models, you use the
# ``get_models()`` function with default parameters. This can be useful for
# cases when you need information about all models in the aWhere API, as
# opposed to a single model.

# Get all models
all_models = awm.get_models(key=awhere_api_key, secret=awhere_api_secret)

###############################################################################
# Get a Single Model
# ------------------
#
# To get a dataframe with a single aWhere model, you use the ``get_models()``
# function and include the specific model ID. This example selects a random
# model ID from the list of all available models.

# Get single model
model = awm.get_models(
    key=awhere_api_key,
    secret=awhere_api_secret,
    model_id=random.choice(awm.MODELS_LIST),
)

###############################################################################
# Get All Model Details
# ---------------------
#
# To get a dataframe with all available aWhere model details, you use the
# ``get_model_details()`` function with default parameters. This can be useful
# for cases when you need information about all models in the aWhere API, as
# opposed to a single model. The ``get_model_details()`` function returns both
# the model base details as well as details about the model stages.

# Get all model details
base_details, stage_details = awm.get_model_details(
    awhere_api_key, awhere_api_secret
)

###############################################################################
# Get Details for a Single Model
# ------------------------------
#
# To get a dataframe with details for a single aWhere model, you use the
# ``get_model_details()`` function and include the specific model ID. This
# example selects a random model ID from the list of all available models. The
# ``get_model_details()`` function returns both the model base details as well
# as details about the model stages.

# Get details for a single model
base_details, stage_details = awm.get_model_details(
    awhere_api_key, awhere_api_secret, model_id=random.choice(awm.MODELS_LIST),
)

###############################################################################
# Get Model Results for a Planted Crop
# ------------------------------------
#
# To get model results for a crop, you must first create an aWhere field
# (using the ``awherepy.crops`` module) and plant a crop associated with that
# field (using the ``awherepy.plantings`` module). You then use the
# ``get_model_results()`` function to get the results of a specified model.

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

# Get model results
results = awm.get_model_results(
    awhere_api_key,
    awhere_api_secret,
    field_id="VT-Manchester",
    model_id="WheatHardRedMSU",
)
