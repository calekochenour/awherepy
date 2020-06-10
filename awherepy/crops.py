"""
awherepy.crops
==============
A module to access and retrieve aWhere crop data.
"""

import requests as rq
import pandas as pd
from pandas.io.json import json_normalize
import awherepy as aw

# Define valid crops
CROPS_LIST = [
    "barley-generic",
    "canola-b-napus",
    "canola-b-rapa",
    "canola-generic",
    "corn-2300-gdd",
    "corn-2500-gdd",
    "corn-2700-gdd",
    "corn-2900-gdd",
    "cotton-2200-gdd",
    "cotton-2600-gdd",
    "green-gram-generic",
    "oat-generic",
    "potato-generic",
    "sorghum-long-season",
    "sorghum-short-season",
    "soya-generic",
    "sugarbeet-generic",
    "sunflower-early-dwarf",
    "sunflower-generic",
    "wheat-generic",
    "wheat-hardred",
]

# Define variables for data cleaning
CROPS_DROP_COLS = [
    "_links.self.href",
    "_links.curies",
    "_links.awhere:plantings.href",
]

CROPS_RENAME_MAP = {
    "id": "crop_id",
    "name": "crop_name",
    "type": "crop_type",
    "variety": "crop_variety",
    "isDefaultForCrop": "default_crop",
}


def get_crops(
    key, secret, crop_id=None,
):
    """Retrieve a list of available crops or single crop if specified.

    API reference:
        https://docs.awhere.com/knowledge-base-docs/crop-list-detail/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    crop_id : str, optional
        Valid aWhere crop id.

    Returns
    -------
    crop_df : pandas dataframe
        Dataframe containing a single crop or all available crops.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.fields as awc
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get all available aWhere crops
        >>> all_crops = awc.get_crops(awhere_api_key, awhere_api_secret)
        >>> # Check number of entries
        >>> len(all_crops)
        21
        >>> # Get a specific crop
        >>> corn_2500_gdd = awc.get_crops(
        >>>     awhere_api_key, awhere_api_secret, crop_id='corn-2500-gdd'
        >>> )
        >>> Check number of entries
        >>> len(corn_2500_gdd)
        1
    """
    # Define global variables
    global CROPS_LIST, CROPS_DROP_COLS, CROPS_RENAME_MAP

    # Define crops api url
    api_url = "https://api.awhere.com/v2/agronomics/crops"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Check if single crop
        if crop_id:

            # Raise error if crop id is invalid
            if crop_id not in CROPS_LIST:
                raise KeyError(
                    (
                        f"Invalid crop id."
                        f"Valid crop ids: {', '.join(CROPS_LIST)}"
                    )
                )

            # Get API response
            response = rq.get(f"{api_url}/{crop_id}", headers=auth_headers)

            # Convert API response to JSON format
            response_json = response.json()

            # Convert to dataframe
            crop_df = json_normalize(response_json)

        # All crops
        else:

            # Initialize variables
            offset = 0
            limit = 10
            pages = 3

            # Initialize list to store dataframe for each page of results
            response_df_list = []

            # Loop through all pages
            while offset < limit * pages:

                # Get API response
                response = rq.get(
                    f"{api_url}?limit={limit}&offset={offset}",
                    headers=auth_headers,
                )

                # Convert API response to JSON format
                response_json = response.json()

                # Convert json to dataframe
                response_df_loop = json_normalize(response_json.get("crops"))

                # Append to dataframe list
                response_df_list.append(response_df_loop)

                # Increase offset by 1 page of results
                offset += limit

            # Merge all page dataframes into a single dataframe
            crop_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary columns
        crop_df.drop(
            columns=CROPS_DROP_COLS, inplace=True,
        )

        # Reset index
        crop_df.reset_index(drop=True, inplace=True)

        # Rename columns
        crop_df.rename(columns=CROPS_RENAME_MAP, inplace=True)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return crop_df
