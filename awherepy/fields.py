"""
awherepy.fields
===============
A module to access and work with aWhere fields.
"""

import requests
from pandas.io.json import json_normalize
import geopandas as gpd
from awherepy import AWhereAPI


class Fields(AWhereAPI):

    # Define columns to drop
    drop_cols = [
        "_links.self.href",
        "_links.curies",
        "_links.awhere:observations.href",
        "_links.awhere:forecasts.href",
        "_links.awhere:plantings.href",
        "_links.awhere:agronomics.href",
    ]

    # Define new column names
    rename_map = {
        "name": "field_name",
        "acres": "area_acres",
        "farmId": "farm_id",
        "id": "field_id",
        "centerPoint.latitude": "center_latitude",
        "centerPoint.longitude": "center_longitude",
    }

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):
        super(Fields, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = "https://api.awhere.com/v2/fields"

    # Modify this to return all fields into a dataframe?
    def get(self, field_id=None, limit=10, offset=0):
        """
        Performs a HTTP GET request to obtain all Fields you've
        created on your aWhere App.

        Docs:
            http://developer.awhere.com/api/reference/fields/get-fields
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Single field
        if field_id:
            # Perform the HTTP request to obtain a specific field
            fields_response = requests.get(
                f"{self.api_url}/{field_id}", headers=auth_headers
            )

        # All fields
        else:
            # Perform the HTTP request to obtain a list of all fields
            fields_response = requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}",
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

        # Drop columns
        fields_df.drop(columns=Fields.drop_cols, inplace=True)

        # Rename columns
        fields_df.rename(columns=Fields.rename_map, inplace=True)

        # Set field ID as index
        fields_df.set_index("field_id", inplace=True)

        # Prep for geodataframe conversion
        df_copy = fields_df.copy()

        # Convert to geodataframe
        fields_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=Fields.crs,
            geometry=gpd.points_from_xy(
                df_copy.center_longitude, df_copy.center_latitude
            ),
        )

        # Drop lat/lon columns
        fields_gdf.drop(
            columns=["center_longitude", "center_latitude"], inplace=True
        )

        # Return geodataframe
        return fields_gdf

    def create(
        self,
        field_id,
        field_name,
        farm_id,
        center_latitude,
        center_longitude,
        acres,
    ):
        """
        Performs a HTTP POST request to create and add a Field to
        your aWhere App.AWhereAPI, based on user input

        Docs:
            http://developer.awhere.com/api/reference/fields/create-field
        """
        field_body = {
            "id": field_id,
            "name": field_name,
            "farmId": farm_id,
            "centerPoint": {
                "latitude": center_latitude,
                "longitude": center_longitude,
            },
            "acres": acres,
        }

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
            "Content-Type": "application/json",
        }

        # Perform the POST request to create Field
        print("Attempting to create field...\n")
        response = requests.post(
            self.api_url, headers=auth_headers, json=field_body
        )

        # Convert API response to JSON
        response_json = response.json()

        # Convert JSON to dataframe
        fields_df = json_normalize(response_json)

        # Drop columns
        fields_df.drop(columns=Fields.drop_cols, inplace=True)

        # Rename columns
        fields_df.rename(columns=Fields.rename_map, inplace=True)

        # Set field ID as index
        fields_df.set_index("field_id", inplace=True)

        # Prep for geodataframe conversion
        df_copy = fields_df.copy()

        # Convert to geodataframe
        fields_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=Fields.crs,
            geometry=gpd.points_from_xy(
                df_copy.center_longitude, df_copy.center_latitude
            ),
        )

        # Drop lat/lon columns
        fields_gdf.drop(
            columns=["center_longitude", "center_latitude"], inplace=True
        )

        # Return geodataframe
        print(f"Created field: {field_id}")
        return fields_gdf

    def update(self, field_id, name=None, farm_id=None):
        """Update the name and/or farm id for a field.
        """
        # Empty update (neither name or farm id)
        if not (name or farm_id):
            field_body = [
                {"op": "replace", "path": "/name", "value": name},
                {"op": "replace", "path": "/farmId", "value": farm_id},
            ]

        # Name only update
        elif name and not farm_id:
            field_body = [{"op": "replace", "path": "/name", "value": name}]

        # Farm id only update
        elif farm_id and not name:
            field_body = [
                {"op": "replace", "path": "/farmId", "value": farm_id}
            ]

        # Name and farm id update
        elif name and farm_id:
            field_body = [
                {"op": "replace", "path": "/name", "value": name},
                {"op": "replace", "path": "/farmId", "value": farm_id},
            ]

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
        }

        # Perform the HTTP request to update field information
        print("Attempting to update field...\n")
        response = requests.patch(
            f"{self.api_url}/{field_id}", headers=auth_headers, json=field_body
        )

        # Convert API response to JSON
        response_json = response.json()

        # Convert JSON to dataframe
        fields_df = json_normalize(response_json)

        # Drop columns
        fields_df.drop(columns=Fields.drop_cols, inplace=True)

        # Rename columns
        fields_df.rename(columns=Fields.rename_map, inplace=True)

        # Set field ID as index
        fields_df.set_index("field_id", inplace=True)

        # Prep for geodataframe conversion
        df_copy = fields_df.copy()

        # Convert to geodataframe
        fields_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=Fields.crs,
            geometry=gpd.points_from_xy(
                df_copy.center_longitude, df_copy.center_latitude
            ),
        )

        # Drop lat/lon columns
        fields_gdf.drop(
            columns=["center_longitude", "center_latitude"], inplace=True
        )

        # Return geodataframe
        print(f"Updated field: {field_id}")
        return fields_gdf

    def delete(self, field_id):
        """
        Performs a HTTP DELETE request to delete a Field from your aWhere App.
        Docs: http://developer.awhere.com/api/reference/fields/delete-field
        Args:
            field_id: The field to be deleted
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

        # Perform the POST request to Ddlete the field
        print("Attempting to delete field...\n")
        response = requests.delete(
            f"{self.api_url}/{field_id}", headers=auth_headers
        )

        # Create output message
        message = (
            f"Deleted field: {field_id}"
            if response.status_code == 204
            else "Could not delete field."
        )

        return print(message)


class Field(Fields):

    # Define columns to drop
    drop_cols = [
        "_links.self.href",
        "_links.curies",
        "_links.awhere:observations.href",
        "_links.awhere:forecasts.href",
        "_links.awhere:plantings.href",
        "_links.awhere:agronomics.href",
    ]

    # Define new column names
    rename_map = {
        "name": "field_name",
        "acres": "area_acres",
        "farmId": "farm_id",
        "id": "field_id",
        "centerPoint.latitude": "center_latitude",
        "centerPoint.longitude": "center_longitude",
    }

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):
        super(Field, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.field_id = field_id
        self.api_url = f"https://api.awhere.com/v2/fields/{self.field_id}"

    def get(self):
        """
        Performs a HTTP GET request to obtain all Fields you've
        created on your aWhere App.

        Docs:
            http://developer.awhere.com/api/reference/fields/get-fields
        """
        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the field information
        field_response = requests.get(f"{self.api_url}", headers=auth_headers)

        # Convert API response to JSON
        response = field_response.json()

        # Convert JSON to dataframe
        field_df = json_normalize(response)

        # Drop columns
        field_df.drop(columns=Field.drop_cols, inplace=True)

        # Rename columns
        field_df.rename(columns=Field.rename_map, inplace=True)

        # Set field ID as index
        field_df.set_index("field_id", inplace=True)

        # Prep for geodataframe conversion
        df_copy = field_df.copy()

        # Convert to geodataframe
        field_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=Field.crs,
            geometry=gpd.points_from_xy(
                df_copy.center_longitude, df_copy.center_latitude
            ),
        )

        # Drop lat/lon columns
        field_gdf.drop(
            columns=["center_longitude", "center_latitude"], inplace=True
        )

        # Return geodataframe
        return field_gdf

    def create(self):
        pass

    def update(self, name=None, farm_id=None):
        """Update the name and/or farm id for a field.
        """
        # Empty update (neither name or farm id)
        if not (name or farm_id):
            field_body = [
                {"op": "replace", "path": "/name", "value": name},
                {"op": "replace", "path": "/farmId", "value": farm_id},
            ]

        # Name only update
        elif name and not farm_id:
            field_body = [{"op": "replace", "path": "/name", "value": name}]

        # Farm id only update
        elif farm_id and not name:
            field_body = [
                {"op": "replace", "path": "/farmId", "value": farm_id}
            ]

        # Name and farm id update
        elif name and farm_id:
            field_body = [
                {"op": "replace", "path": "/name", "value": name},
                {"op": "replace", "path": "/farmId", "value": farm_id},
            ]

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
        }

        # Perform the HTTP request to update field information
        response = requests.patch(
            f"{self.api_url}", headers=auth_headers, json=field_body
        )

        # Convert API response to JSON
        response_json = response.json()

        # Convert JSON to dataframe
        fields_df = json_normalize(response_json)

        # Drop columns
        fields_df.drop(columns=Field.drop_cols, inplace=True)

        # Rename columns
        fields_df.rename(columns=Field.rename_map, inplace=True)

        # Set field ID as index
        fields_df.set_index("field_id", inplace=True)

        # Prep for geodataframe conversion
        df_copy = fields_df.copy()

        # Convert to geodataframe
        fields_gdf = gpd.GeoDataFrame(
            df_copy,
            crs=Field.crs,
            geometry=gpd.points_from_xy(
                df_copy.center_longitude, df_copy.center_latitude
            ),
        )

        # Drop lat/lon columns
        fields_gdf.drop(
            columns=["center_longitude", "center_latitude"], inplace=True
        )

        # Return geodataframe
        print(f"Updated field: {self.field_id}")
        return fields_gdf

    def delete(self):
        """
        Performs a HTTP DELETE request to delete a Field from your aWhere App.
        Docs: http://developer.awhere.com/api/reference/fields/delete-field
        Args:
            field_id: The field to be deleted
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

        # Perform the POST request to Delete the Field
        response = requests.delete(f"{self.api_url}", headers=auth_headers)

        message = (
            f"Deleted field: {self.field_id}"
            if response.status_code == 204
            else "Could not delete field."
        )

        return print(message)
