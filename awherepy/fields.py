"""
awherepy.fields
===============
A module to access and work with aWhere fields.
"""

import requests as rq
from pandas.io.json import json_normalize
import geopandas as gpd
import awherepy as aw

# Define lon/lat columns
FIELD_COORD_COLS = ["centerPoint.longitude", "centerPoint.latitude"]


# Define columns to drop
FIELD_DROP_COLS = [
    "_links.self.href",
    "_links.curies",
    "_links.awhere:observations.href",
    "_links.awhere:forecasts.href",
    "_links.awhere:plantings.href",
    "_links.awhere:agronomics.href",
]

# Define new column names
FIELD_RENAME_MAP = {
    "name": "field_name",
    "acres": "area_acres",
    "farmId": "farm_id",
    "id": "field_id",
}

# Define CRS (EPSG 4326)
FIELD_CRS = "epsg:4326"


def get_field(
    key, secret, field_id=None, query_params={"limit": 10, "offset": 0}
):
    """
    Retrieves all fields or an individual field associated
    with the provided API key/secret.

    Docs:
        http://developer.awhere.com/api/reference/fields/get-fields
    """
    # Define global variables
    global FIELD_COORD_COLS, FIELD_DROP_COLS, FIELD_RENAME_MAP, FIELD_CRS

    # Define fields api url
    api_url = "https://api.awhere.com/v2/fields"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Single field
        if field_id:
            # Perform the HTTP request to obtain a specific field
            fields_response = rq.get(
                f"{api_url}/{field_id}", headers=auth_headers
            )

        # All fields
        else:
            # Perform the HTTP request to obtain a list of all fields
            fields_response = rq.get(
                (
                    f"{api_url}?limit={query_params.get('limit')}"
                    "&offset={query_params.get('offset')}"
                ),
                headers=auth_headers,
            )

        # Convert API response to JSON
        response = fields_response.json()

        # Convert JSON to dataframe
        fields_df = (
            json_normalize(response)
            if field_id
            else json_normalize(response.get("fields"))
        )

        # Prep for geodataframe conversion
        df_copy = fields_df.copy()

        # Convert to geodataframe
        fields_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=FIELD_CRS,
            geometry=gpd.points_from_xy(
                df_copy[FIELD_COORD_COLS[0]], df_copy[FIELD_COORD_COLS[1]]
            ),
        )

        # Add lat/lon columns to drop columns list
        FIELD_DROP_COLS += FIELD_COORD_COLS

        # Drop columns
        fields_gdf.drop(columns=FIELD_DROP_COLS, inplace=True, errors="ignore")

        # Rename columns
        fields_gdf.rename(
            columns=FIELD_RENAME_MAP, inplace=True, errors="ignore"
        )

        # Set field ID as index
        fields_gdf.set_index("field_id", inplace=True)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return geodataframe
    return fields_gdf


def create_field(key, secret, field_info):
    """
    Performs a HTTP POST request to create and add a Field to
    your aWhere App.AWhereAPI, based on user input

    field_info : dict
        Must contain the following keys
            field_id : str
            field_name : str
            farm_id : str
            center_latitude : int or float
            center_longitude : int or float
            acres : int or float

    Docs:
        http://developer.awhere.com/api/reference/fields/create-field
    """
    # Check field_info object type
    if not isinstance(field_info, dict):
        raise TypeError(
            "Invalid type: 'field_info' must be of type dictionary."
        )

    # Raise errors for missing required parameters
    if not field_info.get("field_id"):
        raise KeyError("Missing required field parameter: 'field_id'.")

    if not field_info.get("center_latitude"):
        raise KeyError("Missing required field parameter: 'center_latitude'.")

    if not field_info.get("center_longitude"):
        raise KeyError("Missing required field parameter: 'center_longitude'.")

    # Raise error if field name already exists
    if field_info.get("field_id") in get_field(key, secret).index:
        raise KeyError("Field name already exists within account.")

    # Define fields api url
    api_url = "https://api.awhere.com/v2/fields"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(auth_token)}",
            "Content-Type": "application/json",
        }

        # Define request body
        field_body = {
            "id": field_info.get("field_id"),
            "name": field_info.get("field_name"),
            "farmId": field_info.get("farm_id"),
            "centerPoint": {
                "latitude": field_info.get("center_latitude"),
                "longitude": field_info.get("center_longitude"),
            },
            "acres": field_info.get("acres"),
        }

        # Perform the POST request to create Field
        print("Attempting to create field...\n")
        response = rq.post(api_url, headers=auth_headers, json=field_body)

        # Check if request succeeded
        if response.ok:

            # Get field for output
            field = get_field(key, secret, field_id=field_info.get("field_id"))

            # Indicate success
            print(f"Created field: {field_info.get('field_id')}\n")

        else:

            # Indicate error
            print("Failed to create field.\n")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return created field
    return field


def update_field(key, secret, field_info):
    """Update the field name and/or farm id for a specified field.

    field_info : dict
        Must contain the following keys
            field_id : str
            field_name str
            farm_id: str
    """
    # Check field_info object type
    if not isinstance(field_info, dict):
        raise TypeError(
            "Invalid type: 'field_info' must be of type dictionary."
        )

    # Raise errors for missing required parameters
    if not field_info.get("field_id"):
        raise KeyError("Missing required field parameter: 'field_id'.")

    if not (field_info.get("field_name") or field_info.get("farm_id")):
        raise KeyError(
            (
                "Missing parameter: must update at least one attribute,"
                "'field_name' or 'farm_id'."
            )
        )

    # Raise error if field does not exist
    if field_info.get("field_id") not in get_field(key, secret).index:
        raise KeyError("Field name does not exist within account.")

    # Define fields api url
    api_url = "https://api.awhere.com/v2/fields"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
        }

        # Set up request body
        # Field name and farm id update
        if field_info.get("field_name") and field_info.get("farm_id"):
            field_body = [
                {
                    "op": "replace",
                    "path": "/name",
                    "value": field_info.get("field_name"),
                },
                {
                    "op": "replace",
                    "path": "/farmId",
                    "value": field_info.get("farm_id"),
                },
            ]

        # Field name only update
        elif field_info.get("field_name") and not field_info.get("farm_id"):
            field_body = [
                {
                    "op": "replace",
                    "path": "/name",
                    "value": field_info.get("field_name"),
                }
            ]

        # Farm id only update
        elif field_info.get("farm_id") and not field_info.get("field_name"):
            field_body = [
                {
                    "op": "replace",
                    "path": "/farmId",
                    "value": field_info.get("farm_id"),
                }
            ]

        # Perform the HTTP request to update field information
        print("Attempting to update field...\n")
        response = rq.patch(
            f"{api_url}/{field_info.get('field_id')}",
            headers=auth_headers,
            json=field_body,
        )

        # Check if request succeeded
        if response.ok:

            # Get field for output
            field = get_field(key, secret, field_id=field_info.get("field_id"))

            # Indicate success
            print(f"Updated field: {field_info.get('field_id')}\n")

        else:

            # Indicate error
            print("Failed to create field.\n")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return updated field
    return field


def delete_field(key, secret, field_id):
    """
    Performs a HTTP DELETE request to delete a Field from your aWhere App.
    Docs: http://developer.awhere.com/api/reference/fields/delete-field
    Args:
        field_id: The field to be deleted
    """
    # Raise error if field does not exist
    if field_id not in get_field(key, secret).index:
        raise KeyError("Field name does not exist within account.")

    # Define fields api url
    api_url = "https://api.awhere.com/v2/fields"

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        # Perform the POST request to Ddlete the field
        print("Attempting to delete field...\n")
        rq.delete(f"{api_url}/{field_id}", headers=auth_headers)

        # Check if field exists within account
        try:
            get_field(key, secret, field_id="Test")

        # Catch error if field does not exist (was deleted)
        except KeyError:
            message = print(f"Deleted field: {field_id}")

        # If delete did not work
        else:
            message = print("Could not delete field.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return message
