"""
Get Crop Information with aWherePy
==================================

Learn how to get crop information with aWherePy.

"""

###############################################################################
# Get Crop Information with aWherePy.
# -----------------------------------
#
# .. note::
#    The example below will show you how to use the ``get_crops()`` function to
#    get a list of all available crops or a single crop from the aWhere API.
#
# In this vignette, you will first get all crops, and then you will get a
# single crop by random choice from the list of available crops.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import random
import awherepy.crops as awc

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
# Get All Crops
# -------------
#
# To get a dataframe with all available aWhere crops, you use the
# ``get_crops()`` function with defulat parameters. This can be useful for
# cases when you need information about all crops, in the aWhere API, as
# opposed to a single crop.

# Get all crops
all_crops = awc.get_crops(key=awhere_api_key, secret=awhere_api_secret)

###############################################################################
# Get a Single Crop
# -----------------
#
# To get a dataframe with a single aWhere crop, you use the ``get_crops()``
# function and include the specific crop ID. This example selecte a random crop
# ID from the list of all available crops.

# Get single crop
single_crop = awc.get_crops(
    key=awhere_api_key,
    secret=awhere_api_secret,
    crop_id=random.choice(awc.CROPS_LIST),
)
