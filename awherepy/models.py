"""
awherepy.models
===============
A module to access and retrieve aWhere agronomic model data.
"""

import requests as rq
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
import awherepy as aw
import awherepy.fields as awf

# Define valid models
MODELS_LIST = [
    "BarleyGenericMSU",
    "BarleyGenericNDAWN",
    "CanolaBNapusMSU",
    "CanolaBRapaMSU",
    "CanolaGenericNDAWN",
    "Cotton2600UGCE",
    "Cotton2200NCCA",
    "OatGenericMSU",
    "SugarbeetGenericNDAWN",
    "SunflowerEarlyDwarfMSU",
    "SunflowerGenericNDAWN",
    "WheatHardRedMSU",
    "WheatGenericMAWG",
    "WheatGenericNDAWN",
    "WheatGenericOSU",
    "WheatGenericVCE",
    "Corn2300ISUAbendroth",
    "Corn2500ISUAbendroth",
    "Corn2700ISUAbendroth",
    "Corn2900ISUAbendroth",
    "SorghumShortSeasonTexasAM",
    "SorghumLongSeasonTexasAM",
    "MaizeKALRO",
    "SunflowerH8998KALRO",
    "SunflowerFedhaKALRO",
    "GreenGramKALRO",
    "PotatoKALRO",
    "SorghumKALRO",
    "SoyaKALRO",
]

# Define variables for data cleaning
# Models
MODELS_DROP_COLS = [
    "_links.self.href",
    "_links.curies",
    "_links.awhere:crop",
    "_links.awhere:modelDetails.href",
]

MODELS_RENAME_MAP = {
    "id": "model_id",
    "name": "model_name",
    "description": "model_description",
    "type": "model_type",
    "source.name": "model_source",
    "source.link": "model_link",
}


# Define variables for data cleaning
MODEL_DETAILS_DROP_COLS = [
    "gddUnits",
    "stages",
    "_links.self.href",
    "_links.curies",
    "_links.awhere:model.href",
]

MODEL_DETAILS_BASE_RENAME_MAP = {
    "biofix": "biofix_days",
    "gddMethod": "gdd_method",
    "gddBaseTemp": "gdd_base_temp_cels",
    "gddMaxBoundary": "gdd_max_boundary_cels",
    "gddMinBoundary": "gdd_min_boundary_cels",
}

MODEL_DETAILS_STAGE_RENAME_MAP = {
    "id": "stage_id",
    "stage": "stage_name",
    "description": "stage_description",
    "gddThreshold": "gdd_threshold_cels",
}

# Model results
MODEL_RESULTS_DROP_COLS = ["longitude", "latitude"]

MODEL_RESULTS_RENAME_MAP = {
    "date": "stage_start_date",
    "id": "stage_id",
    "stage": "stage_name",
    "description": "stage_description",
    "gddThreshold": "gdd_threshold_cels",
    "accumulatedGdds": "gdd_accumulation_current_cels",
    "gddRemaining": "gdd_remaining_next_cels",
}

MODEL_RESULTS_REORDER_COLS = [
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


def get_models(key, secret, model_id=None):
    """Retrieve a list of available models or single model if specified.

    API reference: https://docs.awhere.com/knowledge-base-docs/models/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    model_id : str, optional
        Valid aWhere model id.

    Returns
    -------
    model_df : pandas dataframe
        Dataframe containing a single model or all available models.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.models as awm
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get all available aWhere models
        >>> all_models = awm.get_models(awhere_api_key, awhere_api_secret)
        >>> # Display model id for first model
        >>> all_models.index[0]
        BarleyGenericMSU
        >>> # Get a single model
        >>> corn_2700 = awm.get_models(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     modei_id='Corn2700ISUAbendroth'
        ... )
        >>> # Show model name
        >>> corn_2700.model_name
        model_id
        Corn2700ISUAbendroth    Corn, 2700 GDD (Iowa State University)
        Name: model_name, dtype: object
        >>> # Show model type
        >>> corn_2700.model_type
        model_id
        Corn2700ISUAbendroth    GrowthStage
        Name: model_type, dtype: object
    """
    # Define global variables
    global MODELS_LIST, MODELS_DROP_COLS, MODELS_RENAME_MAP

    # Define models api url
    api_url = "https://api.awhere.com/v2/agronomics/models"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Check if single model
        if model_id:

            # Raise error if model id is invalid
            if model_id not in MODELS_LIST:
                raise KeyError(
                    (
                        f"Invalid model."
                        f"Valid models: {', '.join(MODELS_LIST)}"
                    )
                )

            # Get API response
            response = rq.get(f"{api_url}/{model_id}", headers=auth_headers)

            # Convert API response to JSON format
            response_json = response.json()

            # Convert to dataframe
            model_df = json_normalize(response_json)

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
                response_df_loop = json_normalize(response_json.get("models"))

                # Append to dataframe list
                response_df_list.append(response_df_loop)

                # Increase offset by 1 page of results
                offset += limit

            # Merge all page dataframes into a single dataframe
            model_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary columns
        model_df.drop(
            columns=MODELS_DROP_COLS, inplace=True,
        )

        # Reset index
        model_df.reset_index(drop=True, inplace=True)

        # Rename columns
        model_df.rename(columns=MODELS_RENAME_MAP, inplace=True)

        # Set index to model id
        model_df.set_index(keys=["model_id"], drop=True, inplace=True)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return models
    return model_df


def get_model_details(key, secret, model_id=None):
    """Retrieve model details for all available models
    or single model if specified.

    API reference: https://docs.awhere.com/knowledge-base-docs/models/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    model_id : str, optional
        Valid aWhere model id.

    Returns
    -------
    tuple

        base_info_df: pandas dataframe
            Dataframe containing the base information about the model.

        stage_info_df: pandas dataframe
            Dataframe containing the stage information about the model.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.models as awm
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get details for barley generic
        >>> barley_base_details, barley_stage_details = awm.get_model_details(
        ...     awhere_api_key, awhere_api_secret, model_id='BarleyGenericMSU'
        ... )
        >>> # Show base detiils - GDD method
        >>> barley_base_details.gdd_method
        model_id
        BarleyGenericMSU    standard
        Name: gdd_method, dtype: object
        >>> # Show stage names
        >>> barley_stage_details.stage_name
        model_id          stage_id
        BarleyGenericMSU  stage1      Universal 1.0
                          stage2      Universal 1.2
                          stage3      Universal 2.1
                          stage4      Universal 3.1
                          stage5      Universal 6.1
                          stage6      Universal 7.1
                          stage7      Universal 8.5
                          stage8      Universal 8.9
        Name: stage_name, dtype: object
    """
    # Define global variables
    global MODELS_LIST, MODELS_DROP_COLS, MODELS_RENAME_MAP

    # Define models api url
    api_url = "https://api.awhere.com/v2/agronomics/models"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Check if single model
        if model_id:

            # Get API response
            response = rq.get(
                f"{api_url}/{model_id}/details", headers=auth_headers
            )

            # Convert API response to JSON format
            response_json = response.json()

            # Get model base information
            base_info_df = json_normalize(response_json)

            # Drop columns
            base_info_df.drop(
                columns=MODEL_DETAILS_DROP_COLS, inplace=True, errors="ignore"
            )

            # Add model id
            base_info_df["model_id"] = model_id

            # Set index to model id
            base_info_df.set_index("model_id", inplace=True)

            # Rename columns
            base_info_df.rename(
                columns=MODEL_DETAILS_BASE_RENAME_MAP,
                inplace=True,
                errors="ignore",
            )

            # Get model stage information
            stage_info_df = json_normalize(response_json.get("stages"))

            # Drop columns
            stage_info_df.drop(
                columns=MODEL_DETAILS_DROP_COLS, inplace=True, errors="ignore"
            )

            # Add model id
            stage_info_df["model_id"] = model_id

            # Rename columns
            stage_info_df.rename(
                columns=MODEL_DETAILS_STAGE_RENAME_MAP,
                inplace=True,
                errors="ignore",
            )

            # Set multiindex to model id and stage id
            stage_info_df.set_index(["model_id", "stage_id"], inplace=True)

        # All models
        else:

            # Initialize lists to store dataframes
            base_list = []
            stage_list = []

            # Loop through all available models
            for model in list(get_models(key, secret).index):

                # Get API response
                response = rq.get(
                    f"{api_url}/{model}/details", headers=auth_headers
                )

                # Convert API response to JSON format
                response_json = response.json()

                # Get model base information
                base = json_normalize(response_json)

                # Drop columns
                base.drop(
                    columns=MODEL_DETAILS_DROP_COLS,
                    inplace=True,
                    errors="ignore",
                )

                # Add model id
                base["model_id"] = model

                # Set index to model id
                base.set_index("model_id", inplace=True)

                # Rename columns
                base.rename(
                    columns=MODEL_DETAILS_BASE_RENAME_MAP,
                    inplace=True,
                    errors="ignore",
                )

                # Append individual base dataframes to list
                base_list.append(base)

                # Get model stage information
                stage = json_normalize(response_json.get("stages"))

                # Drop columns
                stage.drop(
                    columns=MODEL_DETAILS_DROP_COLS,
                    inplace=True,
                    errors="ignore",
                )

                # Add model id
                stage["model_id"] = model

                # Rename columns
                stage.rename(
                    columns=MODEL_DETAILS_STAGE_RENAME_MAP,
                    inplace=True,
                    errors="ignore",
                )

                # Set multiindex to model id and stage id
                stage.set_index(["model_id", "stage_id"], inplace=True)

                # Append individual stage dataframes to list
                stage_list.append(stage)

            # Merge base and stage dataframes
            base_info_df = pd.concat(base_list, axis=0)
            stage_info_df = pd.concat(stage_list, axis=0)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return base info and stage info dataframes
    return base_info_df, stage_info_df


def get_model_results(key, secret, field_id, model_id):
    """Returns the aWhere agronomic model results
    associated with a specific field and model.

    API reference: https://docs.awhere.com/knowledge-base-docs/models/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_id : str
        Field id for an existing aWhere field.

    model_id : str
        Valid aWhere model id.

    Returns
    -------
    stages_df: pandas dataframe
        Dataframe containing the model results.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import ahwerepy.plantings as awp
        >>> import awherepy.models as awm
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Create planting for Manchester, Vermont field
        >>> vt_planting_info = {
        ...     'crop': 'wheat-hardred',
        ...     'planting_date': '2020-06-01'
        ... }
        >>> awp.create_planting(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     field_id='VT-Manchester',
        ...     planting_info=vt_info
        ... )
        >>> # Get model results
        >>> vt_model_results = awm.get_model_results(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     field_id='VT-Manchester',
        ...     model_id='WheatHardRedMSU'
        ... )
        >>> # Show some columns of model results
        >>> vt_model_results[['stage_description', 'gdd_threshold_cels']]
                                   stage_description  gdd_threshold_cels
        field_id      stage_status
        VT-Manchester Current              emergence               161.0
                      Next          leaf development               206.0
    """
    # Define global variables
    global MODEL_RESULTS_DROP_COLS
    global MODEL_RESULTS_RENAME_MAP
    global MODEL_RESULTS_REORDER_COLS

    # Raise error if field does not exist
    if field_id not in awf.get_fields(key, secret).index:
        raise KeyError("Field name does not exist within account.")

    # Define api url
    api_url = (
        f"https://api.awhere.com/v2/agronomics/fields/"
        f"{field_id}/models/{model_id}/results"
    )

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
        }

        # Get API response
        response = rq.get(f"{api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Get stage info
        # Previous stage
        try:
            # Get info
            previous_stage_df = json_normalize(
                response_json.get("previousStages")
            )

            # Add column
            previous_stage_df["stage_status"] = "Previous"

        # Catch error if no previous stage
        except TypeError:
            previous_stage_df = pd.DataFrame(
                columns=["stage_status"], data=["Previous"]
            )

        # Current stage
        try:
            # Get info
            current_stage_df = json_normalize(
                response_json.get("currentStage")
            )

            # Add column
            current_stage_df["stage_status"] = "Current"

        # Catch error if no current stage
        except TypeError:
            current_stage_df = pd.DataFrame(
                columns=["stage_status"], data=["Current"]
            )

        # Next stage
        try:
            # Get info
            next_stage_df = json_normalize(response_json.get("nextStage"))

            # Add column
            next_stage_df["stage_status"] = "Next"

        # Catch error if no next stage
        except TypeError:
            next_stage_df = pd.DataFrame(
                columns=["stage_status"], data=["Next"]
            )

        # Merge into one dataframe
        stages_df = pd.concat(
            [previous_stage_df, current_stage_df, next_stage_df],
            sort=False,
            axis=0,
        )

        # Change column names
        stages_df.rename(
            columns=MODEL_RESULTS_RENAME_MAP, inplace=True, errors="ignore",
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
        crs = "epsg:4326"

        # Convert to geodataframe
        stages_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(df_copy.longitude, df_copy.latitude),
        )

        # Drop lat/lon
        stages_gdf.drop(
            columns=MODEL_RESULTS_DROP_COLS, inplace=True, errors="ignore"
        )

        # Reorder columns
        stages_gdf = stages_gdf.reindex(columns=MODEL_RESULTS_REORDER_COLS)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return model geodataframe
    return stages_gdf
