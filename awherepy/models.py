"""
awherepy.models
===============
A module to access and retrieve aWhere agronomic model data.
"""

import requests
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
from awherepy.agronomics import Agronomics, AgronomicsField


class AgronomicsModels(Agronomics):
    """Use this API to retrieve agronomic model details.
    """

    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsModels, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.api_url = f"{self.api_url}/models"

    def get(self, model_id=None, limit=10, offset=0):
        """Retrieve a list of available models.
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get API response, single crop or page of crops
        response = (
            requests.get(f"{self.api_url}/{model_id}", headers=auth_headers)
            if model_id
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
            if model_id
            else json_normalize(response_json.get("models"))
        )

        # Drop unnecessary columns
        response_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:crop",
                "_links.awhere:modelDetails.href",
            ],
            inplace=True,
        )

        # Define new column names
        model_rename = {
            "id": "model_id",
            "name": "model_name",
            "description": "model_description",
            "type": "model_type",
            "source.name": "model_source",
            "source.link": "model_link",
        }

        # Rename columns
        response_df.rename(columns=model_rename, inplace=True)

        # Set index
        response_df.set_index("model_id", inplace=True)

        return response_df

    def get_full(self, limit=10, offset=0, max_pages=3):
        """Retrieves the full list of available models,
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
            response_df_loop = json_normalize(response_json.get("models"))
            response_df_list.append(response_df_loop)
            offset += 10

        # Merge all dataframes into a single dataframe
        response_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary columns
        response_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:crop",
                "_links.awhere:modelDetails.href",
            ],
            inplace=True,
        )

        # Define new column names
        model_rename = {
            "id": "model_id",
            "name": "model_name",
            "description": "model_description",
            "type": "model_type",
            "source.name": "model_source",
            "source.link": "model_link",
        }

        # Rename columns
        response_df.rename(columns=model_rename, inplace=True)

        # Set index
        response_df.set_index("model_id", inplace=True)

        return response_df

    def get_details(self, model_id="BarleyGenericMSU"):
        """Retrieve model details
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Get API response, single crop or page of crops
        response = requests.get(
            f"{self.api_url}/{model_id}/details", headers=auth_headers
        )

        # Convert API response to JSON format
        response_json = response.json()

        # Model base information
        base_info_df = json_normalize(response_json)
        base_info_df.drop(
            columns=[
                "gddUnits",
                "stages",
                "_links.self.href",
                "_links.curies",
                "_links.awhere:model.href",
            ],
            inplace=True,
        )
        base_info_df["model_id"] = model_id
        base_info_df.set_index("model_id", inplace=True)
        base_info_df.rename(
            columns={
                "biofix": "biofix_days",
                "gddMethod": "gdd_method",
                "gddBaseTemp": "gdd_base_temp_cels",
                "gddMaxBoundary": "gdd_max_boundary_cels",
                "gddMinBoundary": "gdd_min_boundary_cels",
            },
            inplace=True,
        )

        # Model stage information
        stage_info_df = json_normalize(response_json.get("stages"))
        stage_info_df.drop(columns=["gddUnits"], inplace=True)
        stage_info_df["model_id"] = model_id
        stage_info_df.rename(
            columns={
                "id": "stage_id",
                "stage": "stage_name",
                "description": "stage_description",
                "gddThreshold": "gdd_threshold_cels",
            },
            inplace=True,
        )
        stage_info_df.set_index(["model_id", "stage_id"], inplace=True)

        # Return base info and stage info dataframes
        return base_info_df, stage_info_df

    #     def get_all_details(self):
    #         """Get dataframes with details on all
    #         available models.
    #         """
    #         # Lists to store dataframes
    #         base_list = []
    #         stage_list = []

    #         for model in list(self.get_full().index):
    #             base, stage = self.get_details(model_id=model)
    #             base_list.append(base)
    #             stage_list.append(stage)

    #         base_df_all = pd.concat(base_list, axis=0)
    #         stage_df_all = pd.concat(stage_list, axis=0)

    #         return base_df_all, stage_df_all

    @classmethod
    def get_all_details(cls, api_object):
        """Get dataframes with details on all
        available models.
        """
        # Lists to store dataframes
        base_list = []
        stage_list = []

        # Get all model base info and stage info
        for model in list(api_object.get_full().index):
            base, stage = api_object.get_details(model_id=model)
            base_list.append(base)
            stage_list.append(stage)

        # Merge dataframes
        base_df_all = pd.concat(base_list, axis=0)
        stage_df_all = pd.concat(stage_list, axis=0)

        # Return both dataframes
        return base_df_all, stage_df_all


class AgronomicsFieldModels(AgronomicsField):
    """Use this API to retrieve agronomic model results for a specific field.
    """

    # Define field_id intitializing class
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        model_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsFieldModels, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.field_id = field_id
        self.api_url = (
            f"{self.api_url}/{self.field_id}/models/{model_id}/results"
        )

    def get(self):
        """Returns aWhere model associated with a field.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
            # "Content-Type": 'application/json'
        }

        # Get API response
        response = requests.get(f"{self.api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Get stage info
        previous_stage_df = json_normalize(response_json.get("previousStages"))
        current_stage_df = json_normalize(response_json.get("currentStage"))
        next_stage_df = json_normalize(response_json.get("nextStage"))

        # Add columns
        previous_stage_df["stage_status"] = "Previous"
        current_stage_df["stage_status"] = "Current"
        next_stage_df["stage_status"] = "Next"

        # Merge into one dataframe
        stages_df = pd.concat(
            [previous_stage_df, current_stage_df, next_stage_df],
            sort=False,
            axis=0,
        )

        # Change column names
        stages_df.rename(
            columns={
                "date": "stage_start_date",
                "id": "stage_id",
                "stage": "stage_name",
                "description": "stage_description",
                "gddThreshold": "gdd_threshold_cels",
                "accumulatedGdds": "gdd_accumulation_current_cels",
                "gddRemaining": "gdd_remaining_next_cels",
            },
            inplace=True,
        )

        # Add base data
        stages_df["biofix_date"] = response_json.get("biofixDate")
        stages_df["planting_date"] = response_json.get("plantingDate")
        stages_df["model_id"] = response_json.get("modelId")
        stages_df["field_id"] = response_json.get("location").get("fieldId")
        stages_df["longitude"] = response_json.get("location").get("longitude")
        stages_df["latitude"] = response_json.get("location").get("latitude")

        # Set index
        stages_df.set_index(["field_id", "stage_status"], inplace=True)

        # Prep for geodataframe conversion
        df_copy = stages_df.copy()

        # Define CRS (EPSG 4326)
        crs = {"init": "epsg:4326"}

        # Convert to geodataframe
        stages_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                stages_df.longitude, stages_df.latitude
            ),
        )

        # Drop lat/lon
        stages_gdf.drop(columns=["longitude", "latitude"], inplace=True)

        # Reorder columns
        stages_gdf = stages_gdf.reindex(
            columns=[
                "model_id",
                "biofix_date",
                "planting_date",
                "stage_start_date",
                "stage_id",
                "stage_name",
                "stage_description",
                "gdd_threshold_cels",
                "gdd_accumulation_current_cels",
                "gdd_remaining_next_cels",
                "geometry",
            ]
        )

        return stages_gdf
