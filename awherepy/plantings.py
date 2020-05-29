"""
awherepy.plantings
==================
A module to access and retrieve aWhere agronomic planting data.
"""

import requests
from pandas.io.json import json_normalize
from awherepy.agronomics import Agronomics, AgronomicsField


class AgronomicsPlantings(Agronomics):
    """Use this API to retrieve all the plantings associated with your account.
    """

    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsPlantings, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = f"{self.api_url}/plantings"

    def get(self, planting_id=None, limit=10, offset=0):
        """Returns aWhere plantings associated with your account.

        planting_id can either be an actual id or 'current' for the most
        current planting. 'None' will result in all planting.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
            # "Content-Type": 'application/json'
        }

        # Get API response
        response = (
            requests.get(f"{self.api_url}/{planting_id}", headers=auth_headers)
            if planting_id
            else requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}",
                headers=auth_headers,
            )
        )

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = (
            json_normalize(response_json.get("plantings"))
            if response_json.get("plantings")
            else json_normalize(response_json)
        )

        drop_cols = [
            "_links.self.href",
            "_links.curies",
            "_links.awhere:crop.href",
            "_links.awhere:field.href",
        ]

        # Drop unnecessary columns
        response_df.drop(columns=drop_cols, inplace=True)

        # Define new column names
        planting_rename = {
            "id": "planting_id",
            "crop": "crop_id",
            "field": "field_id",
            "plantingDate": "planting_date",
            "harvestDate": "harvest_date_actual",
            # What is 'recommendation' field? What output goes here,
            # and where does it come from?
            # {response_json.get("yield").get("units").lower()}',
            "yield.amount": "yield_amount_actual",
            "yield.units": "yield_amount_actual_units",
            # {response_json.get("projections").get("yield").get("units").lower()}',
            "projections.yield.amount": "yield_amount_projected",
            "projections.yield.units": "yield_amount_projected_units",
            "projections.harvestDate": "harvest_date_projected",
        }

        # Rename
        response_df.rename(columns=planting_rename, inplace=True)

        # Set index
        response_df.set_index("planting_id", inplace=True)

        return response_df

    def get_full(self):
        """Retrieves the full list of plantings associated
        with an aWhere account.
        """
        pass


class AgronomicsFieldPlantings(AgronomicsField):
    """Use this API to retrieve all the plantings associated with a specific
    field.
    """

    # Define field_id intitializing class
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsFieldPlantings, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/plantings"

    def get(self, planting_id=None, limit=10, offset=0):
        """Returns aWhere plantings associated with a specified field.

        planting_id can either be an actual id or 'current' for the most
        current planting. 'None' will result in all plantings

        GET /v2/agronomics/fields/{fieldId}/plantings
        GET /v2/agronomics/fields/{fieldId}/plantings/{plantingId}
        GET /v2/agronomics/fields/{fieldId}/plantings/current
        """

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
            # "Content-Type": 'application/json'
        }

        # Get API response
        response = (
            requests.get(f"{self.api_url}/{planting_id}", headers=auth_headers)
            if planting_id
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
            if planting_id
            else json_normalize(response_json.get("plantings"))
        )

        drop_cols = [
            "_links.self.href",
            "_links.curies",
            "_links.awhere:crop.href",
            "_links.awhere:field.href",
        ]

        # Drop unnecessary columns
        response_df.drop(columns=drop_cols, inplace=True)

        # Define new column names
        planting_rename = {
            "id": "planting_id",
            "crop": "crop_id",
            "field": "field_id",
            "plantingDate": "planting_date",
            "harvestDate": "harvest_date_actual",
            # What is 'recommendation' field? What output goes here,
            #  and where does it come from?
            # {response_json.get("yield").get("units").lower()}',
            "yield.amount": "yield_amount_actual",
            "yield.units": "yield_amount_actual_units",
            # {response_json.get("projections").get("yield").get("units").lower()}',
            "projections.yield.amount": "yield_amount_projected",
            "projections.yield.units": "yield_amount_projected_units",
            "projections.harvestDate": "harvest_date_projected",
        }

        # Rename
        response_df.rename(columns=planting_rename, inplace=True)

        # Set index
        response_df.set_index("planting_id", inplace=True)

        return response_df

    def create(
        self,
        crop,
        planting_date,
        projected_yield_amount=None,
        projected_yield_units=None,
        projected_harvest_date=None,
        yield_amount=None,
        yield_units=None,
        harvest_date=None,
    ):
        """Creates a planting in the field.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
            "Content-Type": "application/json",
        }

        # Define request body
        field_body = {
            "crop": crop,
            "plantingDate": planting_date,
            "projections": {
                "yield": {
                    "amount": projected_yield_amount,
                    "units": projected_yield_units,
                },
                "harvestDate": projected_harvest_date,
            },
            "yield": {"amount": yield_amount, "units": yield_units},
            "harvestDate": harvest_date,
        }

        # Creat planting
        response = requests.post(
            self.api_url, headers=auth_headers, json=field_body
        )

        return response.json()

    def update(
        self, planting_id="current", update_type="replace", kwargs=None
    ):
        """Update a planting. update_type can be 'replace' or 'update'

        kwargs is a dict with all the update values

        PUT /v2/agronomics/fields/{fieldId}/plantings/{plantingId}
        PUT /v2/agronomics/fields/{fieldId}/plantings/current

        update_kwargs = {
            "crop": 'wheat-hardred',
            "planting_date": '2019-05-20',
            "projected_yield_amount": 90,
            "projected_yield_units": 'small boxes',
            "projected_harvest_date": "2019-08-10",
            "yield_amount": 100,
            "yield_units": "medium boxes",
            "harvest_date": '2019-08-31'
        }

        PATCH /v2/agronomics/fields/{fieldId}/plantings/{plantingId}
        PATCH /v2/agronomics/fields/{fieldId}/plantings/current

        Use dict comprehension for updates
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
            "Content-Type": "application/json",
        }

        # Full replace
        if update_type.lower() == "replace":
            # Define request body
            field_body = {
                "crop": kwargs.get("crop"),
                "plantingDate": kwargs.get("planting_date"),
                "projections": {
                    "yield": {
                        "amount": kwargs.get("projected_yield_amount"),
                        "units": kwargs.get("projected_yield_units"),
                    },
                    "harvestDate": kwargs.get("projected_harvest_date"),
                },
                "yield": {
                    "amount": kwargs.get("yield_amount"),
                    "units": kwargs.get("yield_units"),
                },
                "harvestDate": kwargs.get("harvest_date"),
            }

            # Update planting
            response = requests.put(
                f"{self.api_url}/{planting_id}",
                headers=auth_headers,
                json=field_body,
            )

        elif update_type.lower() == "update":

            # Define field body
            field_body = [
                {"op": "replace", "path": f"/{key}", "value": f"{value}"}
                for key, value in kwargs.items()
            ]

            # Perform the HTTP request to update field information
            response = requests.patch(
                f"{self.api_url}/{planting_id}",
                headers=auth_headers,
                json=field_body,
            )

        else:
            raise ValueError(
                "Invalid update type. Please choose 'replace' or 'update'."
            )

        return response.json()

    def delete(self, planting_id="current"):
        """Deletes a planting, based on planting id or
        the most recent planting (based on id)
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}",
            # "Content-Type": 'application/json'
        }

        # Perform the POST request to Delete the Field
        response = requests.delete(
            f"{self.api_url}/{planting_id}", headers=auth_headers
        )

        message = (
            f"Deleted planting: {planting_id}"
            if response.status_code == 204
            else "Could not delete planting."
        )

        return print(message)
