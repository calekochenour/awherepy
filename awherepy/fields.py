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


def get_fields(key, secret, kwargs=None):
    """
    Returns fields (all or individual) associated with an aWhere application.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    kwargs : dict, optional
        Keyword arguments for different query parameters.
        Running the function without kwargs will use the
        default values. Arguments include:

            field_id: str
                Field ID for a valid aWhere field associated with the input API
                key/secret. Causes the function to return a single field if the
                value is not None. If value is None, all fields associated with
                the API key/secret will be returned. Default value is None.

            limit: int
                Number of results in the API response per page. Used with
                offset kwarg to sort through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Maximum value is 10. Default
                value is 10.

            offset: int
                Number of results in the API response to skip. Used with limit
                kwarg to sorts through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Default value is 0 (start
                with first result).

    Returns
    -------
    fields_gdf : geopandas geodataframe
        Geodataframe containing all fields or an individual field.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.fields as awf
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get all fields associated with key/secret
        >>> all_fields = awf.get_fields(awhere_api_key, awhere_api_secret)
        >>> # Check number of entries in field
        >>> len(all_fields)
        3
        >>> # Define kwargs for single field
        >>> manchester_vt_kwargs = {'field_id': 'Manchester-VT'}
        >>> # Get a single field
        >>> manchester_vt_field = awf.get_fields(
        ...     awhere_api_key, awhere_api_secret, kwargs=manchester_vt_kwargs)
        >>> # Check number of entries
        >>> len(manchester_vt_field)
        1
    """
    # Define global variables
    global FIELD_COORD_COLS, FIELD_DROP_COLS, FIELD_RENAME_MAP, FIELD_CRS

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Check if kwargs is not defined
        if not kwargs:

            # Set limit and offset query parameters
            kwargs = {"limit": 10, "offset": 0}

        # Define fields api url
        api_url = "https://api.awhere.com/v2/fields"

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Single field
        if kwargs.get("field_id"):
            # Perform the HTTP request to obtain a specific field
            fields_response = rq.get(
                f"{api_url}/{kwargs.get('field_id')}", headers=auth_headers
            )

        # All fields
        else:
            # Perform the HTTP request to obtain a list of all fields
            fields_response = rq.get(
                (
                    f"{api_url}?limit={kwargs.get('limit')}"
                    f"&offset={kwargs.get('offset')}"
                ),
                headers=auth_headers,
            )

        # Convert API response to JSON
        response = fields_response.json()

        # Convert JSON to dataframe
        fields_df = (
            json_normalize(response)
            if kwargs.get("field_id")
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
    """Creates a field associated with an aWhere application.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_info : dict
        Dictionary containing the information required to create an aWhere
        field. Can contain the following keys:

            field_id: str, required
                ID for the field. This ID is used to reference the field in
                all applicable aWhere APIs. Can contain only alphanumeric
                characters, underscores, and dashes. Maximum 50 characters.

            center_latitude: int or float, required
                Latitiude (in decimal degrees) of the field center point.

            center_longitude: int or float, required
                Longitude (in decimal degrees) of the field center point.

            farm_id: str, required
                Name of the farm. Not referenced by any other aWhere APIs. Can
                contain only alphanumeric characters, underscores, and dashes.
                Maximum 50 characters.

            field_name: str, optional
                Name of the field. Not referenced by any other aWhere APIs.
                Can contain only alphanumeric characters, underscores, and
                dashes. Maximum 255 characters.

            acres: int or float, optional
                Size of the field in acres.

    Returns
    -------
    field : geopandas geodataframe
        Geodataframe containing the newly-created aWhere field.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.fields as awf
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Define field information for Manchester, Vermont
        >>> manchester_field_info = {
        ...     'field_id': 'VT-Manchester',
        ...     'field_name': 'Manchester-Field',
        ...     'farm_id': 'Manchester-Farm',
        ...     'center_latitude': 43.1636875,
        ...     'center_longitude': -73.0723269,
        ...     'acres': 1
        ... }
        >>> Create field
        >>> field = awf.create_field(
        ...    api_key, api_secret, field_info=manchester_field_info
        ... )
        Attempting to create field...
        Created field: VT-Manchester
        >>> # Check geodataframe index (field id)
        >>> print(field.index[0])
        VT-Manchester
        >>> # Display field
        >>> field
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Check field_info object type
        if not isinstance(field_info, dict):
            raise TypeError(
                "Invalid type: 'field_info' must be of type dictionary."
            )

        # Raise errors for missing required parameters
        if not field_info.get("field_id"):
            raise KeyError("Missing required field parameter: 'field_id'.")

        if not field_info.get("center_latitude"):
            raise KeyError(
                ("Missing required field parameter: 'center_latitude'.")
            )

        if not field_info.get("center_longitude"):
            raise KeyError(
                ("Missing required field parameter: 'center_longitude'.")
            )

        # Raise error if field name already exists
        if field_info.get("field_id") in get_fields(key, secret).index:
            raise KeyError("Field name already exists within account.")

        # Define fields api url
        api_url = "https://api.awhere.com/v2/fields"

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
        print("Attempting to create field...")
        response = rq.post(api_url, headers=auth_headers, json=field_body)

        # Check if request succeeded
        if response.ok:

            # Get field for output
            field = get_fields(
                key, secret, kwargs={"field_id": field_info.get("field_id")}
            )

            # Indicate success
            print(f"Created field: {field_info.get('field_id')}")

        else:

            # Indicate error
            print("Failed to create field.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return created field
    return field


def update_field(key, secret, field_info):
    """Update the field name and/or farm id for a specified field.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_info : dict
        Dictionary containing information required to update the field. Must
        provide an update to field_name or farm_id (cannot make empty update).
        Can contain the following keys:

            field_id: str, required
                Field ID for an existing aWhere field. This identifies the
                field that will be updated.

            field_name: str, required if farm_id not specified
                Updated field name.

            farm_id: str, required if field_name is not specified
                Updated farm ID.

    Returns
    -------
    field : geopandas geodataframe
        Geodataframe containing the updated aWhere field.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.fields as awf
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Define update parameters for Manchester, Vermont
        >>> manchester_update_info = {
        ...     'field_id': 'VT-Manchester',
        ...     'field_name': 'Manchester-Field-Update',
        ...     'farm_id': 'Manchester-Farm-Update'
        ... }
        >>> # Update the field
        >>> field_updated = awf.update_field(
        ...     api_key, api_secret,
        ...     field_info=manchester_update_info
        ... )
        Attempting to update field...
        Updated field: VT-Manchester
        >>> # Display updated field
        >>> field_updated
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

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
        if field_info.get("field_id") not in get_fields(key, secret).index:
            raise KeyError("Field name does not exist within account.")

        # Define fields api url
        api_url = "https://api.awhere.com/v2/fields"

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
        print("Attempting to update field...")
        response = rq.patch(
            f"{api_url}/{field_info.get('field_id')}",
            headers=auth_headers,
            json=field_body,
        )

        # Check if request succeeded
        if response.ok:

            # Get field for output
            field = get_fields(
                key, secret, kwargs={"field_id": field_info.get("field_id")}
            )

            # Indicate success
            print(f"Updated field: {field_info.get('field_id')}")

        else:
            # Indicate error
            field = print("Failed to update field.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return updated field
    return field


def delete_field(key, secret, field_id):
    """
    Deletes a speficied aWhere field.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_id : str
        Field ID for an existing aWhere field. This identifies the field that
        will be deleted from the aWhere application.

    Returns
    -------
    message : str
        Output message indicating success or failure for the field deletion.

    Example
    -------
    >>> # Imports
    >>> import os
    >>> import awherepy as aw
    >>> import awherepy.fields as awf
    >>> # Get aWhere API key and secret
    >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
    >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
    >>> # Delete field for Manchester, Vermont
    >>> awf.delete_field(
    ...     awhere_api_key, awhere_api_secret, field_id='VT-Manchester'
    ... )
    Attempting to delete field...
    Deleted field: VT-Manchester
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Raise error if field does not exist
        if field_id not in get_fields(key, secret).index:
            raise KeyError("Field name does not exist within account.")

        # Define fields api url
        api_url = "https://api.awhere.com/v2/fields"

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
        }

        # Perform the POST request to Ddlete the field
        print("Attempting to delete field...")
        rq.delete(f"{api_url}/{field_id}", headers=auth_headers)

        # Check if field exists within account
        try:
            get_fields(key, secret, kwargs={"field_id": field_id})

        # Catch error if field does not exist (was deleted)
        except KeyError:
            message = f"Deleted field: {field_id}"
            print(message)

        # If delete did not work
        else:
            message = "Could not delete field."
            print(message)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return message
