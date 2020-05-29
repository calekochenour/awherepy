"""
awherepy.crops
==============
A module to access and retrieve aWhere crop data.
"""

import requests
import pandas as pd
from pandas.io.json import json_normalize
from awherepy.agronomics import Agronomics


class AgronomicsCrops(Agronomics):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsCrops, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.api_url = f"{self.api_url}/crops"

    # field_id=None, crop_name=None, limit=10, offset=0
    def get(self, crop_id=None, limit=10, offset=0):
        """Retrieve a list of available crops.
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get API response, single crop or page of crops
        response = (
            requests.get(f"{self.api_url}/{crop_id}", headers=auth_headers)
            if crop_id
            else requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}",
                headers=auth_headers,
            )
        )

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = (
            json_normalize(response_json)
            if crop_id
            else json_normalize(response_json.get("crops"))
        )

        # Drop unnecessary columns
        response_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:plantings.href",
            ],
            inplace=True,
        )

        # Reset index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column names
        crop_rename = {
            "id": "crop_id",
            "name": "crop_name",
            "type": "crop_type",
            "variety": "crop_variety",
            "isDefaultForCrop": "default_crop",
        }

        # Rename columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df

    def get_full(self, limit=10, offset=0, max_pages=3):
        """Retrieves the full list of available crops,
        based on limit, offset, and max pages.
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Define list to store page dataframes
        response_df_list = []

        # Loop through all pages
        while offset < limit * max_pages:

            # Get API response; convert response to dataframe; append
            #  to dataframe list
            response = requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}",
                headers=auth_headers,
            )
            response_json = response.json()
            response_df_loop = json_normalize(response_json.get("crops"))
            response_df_list.append(response_df_loop)
            offset += 10

        # Merge all dataframes into a single dataframe
        response_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary dataframe columns
        response_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:plantings.href",
            ],
            inplace=True,
        )

        # Reset dataframe index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column name mapping
        crop_rename = {
            "id": "crop_id",
            "name": "crop_name",
            "type": "crop_type",
            "variety": "crop_variety",
            "isDefaultForCrop": "default_crop",
        }

        # Rename dataframe columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df


class AgronomicsCrop(AgronomicsCrops):
    def __init__(
        self,
        api_key,
        api_secret,
        crop_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsCrop, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.api_url = f"{self.api_url}/{crop_id}"

    def get(self):
        """Retrieves the information for the defined crop.
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get API response, single crop
        response = requests.get(f"{self.api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json)

        # Drop unnecessary columns
        response_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:plantings.href",
            ],
            inplace=True,
        )

        # Reset index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column names
        crop_rename = {
            "id": "crop_id",
            "name": "crop_name",
            "type": "crop_type",
            "variety": "crop_variety",
            "isDefaultForCrop": "default_crop",
        }

        # Rename columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df
