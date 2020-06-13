"""
awherepy.plantings
==================
A module to access and retrieve aWhere agronomic planting data.
"""

import requests as rq
from pandas.io.json import json_normalize
import awherepy as aw
import awherepy.fields as awf

# Define variables for data cleaning
PLANTINGS_DROP_COLS = [
    "_links.self.href",
    "_links.curies",
    "_links.awhere:crop.href",
    "_links.awhere:field.href",
]

PLANTINGS_RENAME_MAP = {
    "id": "planting_id",
    "crop": "crop_id",
    "field": "field_id",
    "plantingDate": "planting_date",
    "harvestDate": "harvest_date_actual",
    "yield.amount": "yield_amount_actual",
    "yield.units": "yield_amount_actual_units",
    "projections.yield.amount": "yield_amount_projected",
    "projections.yield.units": "yield_amount_projected_units",
    "projections.harvestDate": "harvest_date_projected",
}


def create_planting(key, secret, field_id, planting_info):
    """Creates a planting in an aWhere field.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_id : str
        Field ID for an existing aWhere field.

    planting_info : dict
        Dictionary containing the information required to create an aWhere
        planting. Can contain the following keys:

            crop: str, required
                ID for the crop that will be planted. Must be a valid aWhere
                crop ID.

            planting_date: str, required
                Planting date for the crop, formatted as 'YYYY-MM-DD'.

            projected_yield_amount: str or int or float, optional
                Projected yield amount for the crop. If used, the
                projected_yield_units parameter must also be set.

            projected_yield_units: str, optional
                Units for the projected crop yield. If used, the
                projected_yield_amount parameter must also be set.

            projected_harvest_date: str, optional
                Projected harvest date for the crop, formatted as
                'YYYY-MM-DD'.

            yield_amount: str or int or float, optional
                Actual yield amount for the crop. If used, the
                yield_units parameter must also be set.

            yield_units: str, optional
                Units for the actual crop yield. If used, the
                yield_amount parameter must also be set.

            harvest_date: str, optional
                Actual harvest date for the crop, formatted as 'YYYY-MM-DD'.

    Returns
    -------
    planting : pandas dataframe
        Dataframe containing the planting information.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import ahwerepy.plantings as awp
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Create planting for Manchester, Vermont field
        >>> vt_planting_info = {
        ...     'crop': 'potato-generic',
        ...     'planting_date': '2020-05-01',
        ...     'projected_harvest_date': '2020-09-30',
        ...     'projected_yield_amount': 200,
        ...     'projected_yield_units': 'boxes'
        ... }
        >>> awp.create_planting(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     field_id='VT-Manchester',
        ...     planting_info=vt_planting_info
        ... )
        Attempting to create planting...
        Created planting: potato-generic planted in VT-Manchester

                            crop_id         field_id    planting_date
        planting_id
        # potato-generic    VT-Manchester       2020-05-01
    """
    # Check planting_info object type
    if not isinstance(planting_info, dict):
        raise TypeError(
            "Invalid type: 'planting_info' must be of type dictionary."
        )

    # Raise errors for missing required parameters
    if not planting_info.get("crop"):
        raise KeyError("Missing required planting parameter: 'crop'.")

    if not planting_info.get("planting_date"):
        raise KeyError("Missing required planting parameter: 'planting_date'.")

    if planting_info.get("projected_yield_amount") and not planting_info.get(
        "projected_yield_units"
    ):
        raise KeyError(
            "Missing required planting parameter: 'projected_yield_units'."
        )

    if planting_info.get("projected_yield_units") and not planting_info.get(
        "projected_yield_amount"
    ):
        raise KeyError(
            "Missing required planting parameter: 'projected_yield_amount'."
        )

    if planting_info.get("yield_amount") and not planting_info.get(
        "yield_units"
    ):
        raise KeyError("Missing required planting parameter: 'yield_units'.")

    if planting_info.get("yield_units") and not planting_info.get(
        "yield_amount"
    ):
        raise KeyError("Missing required planting parameter: 'yield_units'.")

    # Define plantings api url
    api_url = (
        f"https://api.awhere.com/v2/agronomics/fields/{field_id}/plantings"
    )

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        # Define request body
        field_body = {
            "crop": planting_info.get("crop"),
            "plantingDate": planting_info.get("planting_date"),
            "projections": {
                "yield": {
                    "amount": planting_info.get("projected_yield_amount"),
                    "units": planting_info.get("projected_yield_units"),
                },
                "harvestDate": planting_info.get("projected_harvest_date"),
            },
            "yield": {
                "amount": planting_info.get("yield_amount"),
                "units": planting_info.get("yield_units"),
            },
            "harvestDate": planting_info.get("harvest_date"),
        }

        # Perform the POST request to create Field
        print("Attempting to create planting...")
        response = rq.post(api_url, headers=auth_headers, json=field_body)

        # Check if request succeeded
        if response.ok:

            # Get planting for output
            planting = get_plantings(
                key,
                secret,
                field_id=planting_info.get("field_id"),
                planting_id="current",
            )

            # Indicate success
            print(
                (
                    f"Created planting: {planting_info.get('crop')}"
                    f"planted in {field_id}"
                )
            )

        else:

            # Indicate error
            print("Failed to create field.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return planting
    return planting


def get_plantings(key, secret, kwargs=None):
    """Gets all aWhere plantings associated an account, all plantings
    associated with a with a specified field, or an individual planting.

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
                key/secret. If not specified and planting_id not specified,
                all plantings for all fields will be returned. If specified and
                planting_id not specified, all plantings associated with the
                specific field will be returned.

            planting_id: int
                Planting ID for a valid planting associated with an existing
                aWhere field. If specified and field_specified, a single
                planting will be returned. If not specified and field_id
                specified, the current (most recent) planting for that field
                will be returned.

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
    plantings_df : pandas dataframe
        Dataframe containing all plantings or an individual planting.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import ahwerepy.plantings as awp
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get all plantings in all fields
        >>> all_plantings = awp.get_plantings(
        ...     awhere_api_key, awhere_api_secret
        ... )
        >>> # Get all plantings for a specific field
        >>> vt_plantings = awp.get_plantings(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     kwargs={'field_id': 'VT-Manchester'}
        ... )
        >>> # Get most recent planting (looks through all fields)
        >>> current_planting = awp.get_plantings(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     kwargs={'planting_id': 'current'}
        ... )
        >>> # Get specific planting
        >>> vt_planting = awp.get_plantings(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     kwargs={'planting_id': ######}
        ... )
    """
    # Define global variables
    global PLANTINGS_DROP_COLS, PLANTINGS_RENAME_MAP

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # All plantings from all fields
        if not kwargs:

            # Set limit and offset query parameters
            kwargs = {"limit": 10, "offset": 0}

            # Define api url
            api_url = (
                "https://api.awhere.com/v2/agronomics/plantings?limit="
                f"{kwargs.get('limit')}&offset={kwargs.get('offset')}"
            )

        # All plantings from single field
        elif kwargs.get("field_id") and not kwargs.get("planting_id"):

            # Set limit and offset query parameters if not existing
            if "limit" not in kwargs.keys():
                kwargs["limit"] = 10

            if "offset" not in kwargs.keys():
                kwargs["offset"] = 0

            # Define api url
            api_url = (
                "https://api.awhere.com/v2/agronomics/fields/"
                f"{kwargs.get('field_id')}/plantings"
            )

        # Single planting (id/current), field-independent
        elif kwargs.get("planting_id") and not kwargs.get("field_id"):

            # Define api url
            api_url = (
                "https://api.awhere.com/v2/agronomics/plantings/"
                f"{kwargs.get('planting_id')}"
            )

        # Invalid combination
        else:

            # Raise error
            raise KeyError("Invalid kwarg combination.")

        # Get API response
        response = rq.get(f"{api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        plantings_df = (
            json_normalize(response_json.get("plantings"))
            if response_json.get("plantings")
            else json_normalize(response_json)
        )

        # Drop unnecessary columns
        plantings_df.drop(
            columns=PLANTINGS_DROP_COLS, inplace=True, errors="ignore"
        )

        # Rename columns
        plantings_df.rename(
            columns=PLANTINGS_RENAME_MAP, inplace=True, errors="ignore"
        )

        # Set index
        plantings_df.set_index("planting_id", inplace=True)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return the plantings dataframe
    return plantings_df


def update_planting(
    key, secret, planting_info,
):
    """Updates a specified planting.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    planting_info : dict
        Dictionary containing the information to update an aWhere planting.
        Can contain the following keys:

            field_id: str
                Field ID for an existing aWhere field.

            planting_id: int
                Planting ID for an existing planting.

            update_type : str
                The type of update. Options are 'full' or 'partial'. Full
                update replaces every parameter in the planting. Partial
                update replaces only the provided parameters in the planting.

            crop: str
                ID for the crop that will be planted. Must be a valid aWhere
                crop ID.

            planting_date: str, required
                Planting date for the crop, formatted as 'YYYY-MM-DD'.

            projected_yield_amount: str or int or float, optional
                Projected yield amount for the crop. If used, the
                projected_yield_units parameter must also be set.

            projected_yield_units: str, optional
                Units for the projected crop yield. If used, the
                projected_yield_amount parameter must also be set.

            projected_harvest_date: str, optional
                Projected harvest date for the crop, formatted as
                'YYYY-MM-DD'.

            yield_amount: str or int or float, optional
                Actual yield amount for the crop. If used, the
                yield_units parameter must also be set.

            yield_units: str, optional
                Units for the actual crop yield. If used, the
                yield_amount parameter must also be set.

            harvest_date: str, optional
                Actual harvest date for the crop, formatted as 'YYYY-MM-DD'.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import ahwerepy.plantings as awp
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Define planting update information
        >>> planting_update_info = {
        ...     'field_id': 'VT-Manchester',
        ...     'planting_id': 475994,
        ...     'update_type': 'partial'
        ...     'crop': 'sugarbeet-generic',
        ...     'planting_date': '2020-06-05',
        ...     'projections_yield_amount': 50,
        ...     'projections_yield_units': 'large boxes',
        ...     'projected_harvest_date': '2020-08-08',
        ...     'yield_amount': 200,
        ...     'yield_units': 'large boxes',
        ...     'harvest_date': '2020-07-31'
        ... }
        >>> # Update planting
        >>> awp.update_planting(
        ...     awhere_api_key,
        ...     awhere_api_secret,
        ...     planting_info=planting_update_info
        ... )
        Attempting to update planting...
        Updated planting: sugarbeet-generic in VT-Manchester
    """
    # Check planting_info object type
    if not isinstance(planting_info, dict):
        raise TypeError(
            "Invalid type: 'planting_info' must be of type dictionary."
        )

    # Raise error if field does not exist
    if planting_info.get("field_id") not in awf.get_fields(key, secret).index:
        raise KeyError("Field does not exist within account.")

    # Raise error if planting does not exist
    if planting_info.get("planting_id") != "current":
        if (
            planting_info.get("planting_id")
            not in get_plantings(key, secret).index
        ):
            raise KeyError("Planting does not exist within account.")

    # Raise error if update type is not valid
    if planting_info.get("update_type") not in ["full", "partial"]:
        raise ValueError("Invalid update type. Must be 'full' or 'partial'.")

    # Define api url
    api_url = (
        "https://api.awhere.com/v2/agronomics/fields/"
        f"{planting_info.get('field_id')}/plantings/"
        f"{planting_info.get('planting_id')}"
    )

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Set up the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json",
        }

        # Full update
        if planting_info.get("update_type").lower() == "full":

            # Define request body
            field_body = {
                "crop": planting_info.get("crop"),
                "plantingDate": planting_info.get("planting_date"),
                "projections": {
                    "yield": {
                        "amount": planting_info.get("projected_yield_amount"),
                        "units": planting_info.get("projected_yield_units"),
                    },
                    "harvestDate": planting_info.get("projected_harvest_date"),
                },
                "yield": {
                    "amount": planting_info.get("yield_amount"),
                    "units": planting_info.get("yield_units"),
                },
                "harvestDate": planting_info.get("harvest_date"),
            }

            # Perform HTTP request to update planting information
            print("Attempting to update planting...")
            response = rq.put(
                f"{api_url}", headers=auth_headers, json=field_body,
            )

        # Partial update
        elif planting_info.get("update_type").lower() == "partial":

            # Define field body
            field_body = [
                {"op": "replace", "path": f"/{key}", "value": f"{value}"}
                for key, value in planting_info.items()
            ]

            # Perform HTTP request to update planting information
            print("Attempting to update planting...")
            response = rq.patch(
                f"{api_url}", headers=auth_headers, json=field_body,
            )

        # Invalid update type
        else:
            raise ValueError(
                "Invalid update type. Please choose 'full' or 'partial'."
            )

        # Check if request succeeded
        if response.ok:

            # Get planting for output
            planting = get_plantings(
                key,
                secret,
                field_id=planting_info.get("field_id"),
                planting_id=planting_info.get("planting_id"),
            )

            # Indicate success
            print(
                (
                    f"Updated planting: {planting_info.get('planting_id')}"
                    f"in {planting_info.get('field_id')}"
                )
            )

        else:
            # Indicate error
            planting = print("Failed to update planting.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return planting
    return planting


def delete_planting(key, secret, field_id, planting_id="current"):
    """Deletes a specified aWhere planting.

    API reference: https://docs.awhere.com/knowledge-base-docs/field-plantings/

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    field_id : str
        Field ID for an existing aWhere field.

    planting_id : int, optional
        Planting ID for an existing planting. This identifies the planting that
        will be deleted from the specified aWhere field. Default value is
        'current', which references the most recent planting associated with
        the specified field.

    Returns
    -------
    message : str
        Output message indicating success or failure for the planting deletion.

    Example
    -------
    >>> # Imports
    >>> import os
    >>> import awherepy as aw
    >>> import awherepy.plantings as awp
    >>> # Get aWhere API key and secret
    >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
    >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
    >>> # Delete planting in Manchester, Vermont field
    >>> awp.delete_planting(
    ...     awhere_api_key,
    ...     awhere_api_secret,
    ...     field_id='VT-Manchester',
    ...     planting_id=######
    ... )
    Attempting to delete planting...
    Deleted planting: ###### in VT-Manchester
    """
    # Raise error if field does not exist
    if field_id not in awf.get_fields(key, secret).index:
        raise KeyError("Field name does not exist within account.")

    # Raise error if planting does not exist
    if planting_id != "current":
        if planting_id not in get_plantings(key, secret).index:
            raise KeyError("Planting does not exist within account.")

    # Define api url
    api_url = (
        f"https://api.awhere.com/v2/agronomics/fields/"
        f"{field_id}/plantings/{planting_id}"
    )

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {auth_token}",
        }

        # Perform the POST request to delete the planting
        print("Attempting to delete planting...")
        rq.delete(f"{api_url}", headers=auth_headers)

        # Check if planting exists within account
        try:
            get_plantings(
                key, secret, field_id=field_id, planting_id=planting_id
            )

        # Catch error if planting does not exist (was deleted)
        except KeyError:
            message = print(f"Deleted planting: {planting_id} in {field_id}")

        # If delete did not work
        else:
            message = print("Could not delete planting.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return message
