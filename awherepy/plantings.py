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

    planting_info : dict
        Dictionary containing the information required to create an aWhere
        planting. Can contain the following keys:

            crop: str, required
                ID for the field. This ID is used to reference the field in
                all applicable aWhere APIs. Can contain only alphanumeric
                characters, underscores, and dashes. Maximum 50 characters.

            planting_date: str, required
                'YYYY-MM-DD'

            projected_yield_amount: str, optional

            projected_yield_units: str, optional

            projected_harvest_date: str, optional
                'YYYY-MM-DD'. Projected harvest date.

            yield_amount: str, optional

            yield_units: str, optional

            harvest_date: str, optional
                Actual harvest date.
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


def get_plantings(
    key, secret, field_id=None, planting_id=None, limit=10, offset=0
):
    """Gets all aWhere plantings associated an account, all plantings
    associated with a with a specified field, or an individual planting
    associated with a specific field.
    """
    # Raise error if planting does not exist
    if planting_id is not None and planting_id != "current":
        if planting_id not in get_plantings(key, secret).index:
            raise KeyError("Planting does not exist within account.")

    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get OAuth token
        auth_token = aw.get_oauth_token(key, secret)

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {auth_token}"}

        # Check if field id specified
        if field_id:

            # Raise error if invalid field id
            if field_id not in awf.get_fields(key, secret).index:
                raise KeyError("Field does not exist within account.")

            # Define fields base url
            fields_url = "https://api.awhere.com/v2/agronomics/fields"

            # Define field-specific api url
            api_url = (
                f"{fields_url}/{field_id}/plantings/{planting_id}"
                if planting_id
                else f"{fields_url}/{field_id}/plantings"
            )

        # No field specified
        else:

            # Define non-fields base url
            non_field_url = "https://api.awhere.com/v2/agronomics/plantings"

            # Defune non-fields-specific url
            api_url = (
                f"{non_field_url}/{planting_id}"
                if planting_id == "current"
                else f"{non_field_url}"
            )

        # Get API response
        response = rq.get(
            f"{api_url}?limit={limit}&offset={offset}", headers=auth_headers
        )

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        plantings_df = (
            json_normalize(response_json.get("plantings"))
            if response_json.get("plantings")
            else json_normalize(response_json)
        )

        # Drop unnecessary columns
        plantings_df.drop(columns=PLANTINGS_DROP_COLS, inplace=True)

        # Rename columns
        plantings_df.rename(columns=PLANTINGS_RENAME_MAP, inplace=True)

        # Set index
        plantings_df.set_index("planting_id", inplace=True)

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return the plantings dataframe
    return plantings_df


def update_planting(
    key,
    secret,
    field_id,
    planting_info,
    planting_id="current",
    update_type="full",
):
    """Updates a specified planting.
    """
    # Check planting_info object type
    if not isinstance(planting_info, dict):
        raise TypeError(
            "Invalid type: 'planting_info' must be of type dictionary."
        )

    # Raise error if field does not exist
    if field_id not in awf.get_fields(key, secret).index:
        raise KeyError("Field does not exist within account.")

    # Raise error if planting does not exist
    if planting_id != "current":
        if planting_id not in get_plantings(key, secret).index:
            raise KeyError("Planting does not exist within account.")

    # Raise error if update type is not valid
    if update_type not in ["full", "partial"]:
        raise ValueError("Invalid update type. Must be 'full' or 'partial'.")

    # Define api url
    api_url = (
        f"https://api.awhere.com/v2/agronomics/fields/"
        f"{field_id}/plantings/{planting_id}"
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
        if update_type.lower() == "full":

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
        elif update_type.lower() == "partial":

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
                planting_id=planting_id,
            )

            # Indicate success
            print(f"Updated planting: {planting_id} in {field_id}")

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
            message = print(f"Deleted planting: {planting_id}")

        # If delete did not work
        else:
            message = print("Could not delete planting.")

    # Invalid credentials
    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return message
