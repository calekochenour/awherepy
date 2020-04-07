""" Defines a class and methods to call aWhere API """

# Imports
import base64
import requests


class AWhereAPI():
    def __init__(self, api_key, api_secret):
        """
        Initializes the AWhereAPI class, which is used to
        perform HTTP requests to the aWhere V2 API.

        Docs:
            http://developer.awhere.com/api/reference

        Parameters
        ----------
        api_key : str
            API key for aWhere app.

        api_secret : str
            API secret for aWhere.

        Returns
        -------
        None

        Example
        -------
        awhere = AWhereAPI('test_key', 'test_secret')
        """
        # Define API URLs
        self._fields_url = 'https://api.awhere.com/v2/fields'
        self._weather_url = 'https://api.awhere.com/v2/weather/fields'
        self._plantings_url = 'https://api.awhere.com/v2/agronomics/plantings'
        self._agronomics_url = 'https://api.awhere.com/v2/agronomics/fields'
        self._crops_url = 'https://api.awhere.com/v2/agronomics/fields/v2/agronomics/crops'
        self._models_url = 'https://api.awhere.com//v2/agronomics/models'

        # Define authorization information
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_64_encoded_secret_key = self.encode_secret_and_key(
            self.api_key, self.api_secret)
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)

    def create_field(self, field_id, field_name, farm_id, center_latitude, center_longitude, acres):
        """
        Performs a HTTP POST request to create and add a Field to your aWhere App.AWhereAPI, based on user input

        Docs:
            http://developer.awhere.com/api/reference/fields/create-field
        """
        field_body = {
            'id': field_id,
            'name': field_name,
            'farmId': farm_id,
            'centerPoint': {
                'latitude': center_latitude,
                'longitude': center_longitude
            },
            'acres': acres
        }

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
            "Content-Type": 'application/json'
        }

        # Perform the POST request to create Field
        print('Attempting to create new field....\n')
        response = requests.post(
            self._fields_url, headers=auth_headers, json=field_body)

        if response.status_code == 201:
            print(f"Your field {field_id} was successfully created!")
        else:
            print("An error occurred. Please review the above resonse and try again.")

        # return response.json() # Return the JSON formatted response

    def delete_field_by_id(self, field_id):
        """
        Performs a HTTP DELETE request to delete a Field from your aWhere App.
        Docs: http://developer.awhere.com/api/reference/fields/delete-field
        Args:
            field_id: The field to be deleted
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": 'application/json'
        }
        # Perform the POST request to Delete the Field
        response = requests.delete(
            f"{self._fields_url}/{field_id}",
            headers=auth_headers)

        print(f"The server responded with a status code of {response.status_code}")

    def encode_secret_and_key(self, key, secret):
        """
        Docs:
            http://developer.awhere.com/api/authentication
        Returns:
            Returns the base64-encoded {key}:{secret} combination, seperated by a colon.
        """
        # Base64 Encode the Secret and Key
        key_secret = f"{key}:{secret}"

        encoded_key_secret = base64.b64encode(
            bytes(key_secret, 'utf-8')).decode('ascii')

        return encoded_key_secret

    def get_fields(self):
        """
        Performs a HTTP GET request to obtain all Fields you've created on your aWhere App.

        Docs:
            http://developer.awhere.com/api/reference/fields/get-fields
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain a list of all Fields
        fields_response = requests.get(self._fields_url,
                                       headers=auth_headers)

        responseJSON = fields_response.json()

        # Display the count of Fields for the user account
        print(f"You have {len(responseJSON['fields'])} fields registered on your account")

        # Iterate over the fields and display their name and ID
        print('#  Field Name \t\t Field ID')
        print('-------------------------------------------')
        count = 0
        for field in responseJSON["fields"]:
            count += 1
            print(f"{count}. {field['name']} \t {field['id']}\r")

    def get_weather_forecast(self, field_id):
        """
        Performs a HTTP GET request to obtain the 7-day forecast.

        Docs:
            http://developer.awhere.com/api/forecast-weather-api

        Parameters
        ----------
        field_id : str
            ID of the field.

        Returns
        -------
        response: dict
            Dictionary containing the forecast.

        Example
        -------
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the Forecast for the Field
        response = requests.get(
            f"{self._weather_url}/{field_id}/forecasts?blockSize=24",
            headers=auth_headers)

        # Return forecast
        return response.json()

    def get_weather_norms(self, field_id, start_day, end_day=None, offset=0):
        """
        Performs a HTTP GET request to obtain 10-year historical norms.

        Docs:
            http://developer.awhere.com/api/reference/weather/norms

        Parameters
        ----------
        field_id : str
            ID of the field.

        Returns
        -------
        response : dict
            Dictionary containing the norms.

        Example
        -------
        """
        """# Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        response = requests.get(
            f"{self._weather_url}/{field_id}/norms/{start_day}",
            headers=auth_headers)

        # Return the norms
        return response.json()"""

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self._weather_url}/{field_id}/norms/{start_day}?limit=10&offset={offset}"
        url_multiple_days = f"{self._weather_url}/{field_id}/norms/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    def get_weather_observed(self, field_id, start_day=None, end_day=None, offset=0):
        """
        Performs a HTTP GET request to obtain 7-day observed weather.

        Docs:
            http://developer.awhere.com/api/reference/weather/observations

        Parameters
        ----------
        field_id : str
            ID of the field.

        Returns
        -------
        response : dict
            Dictionary containing the observed weather.

        Example
        -------
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Define URL variants
        url_no_date = f"{self._weather_url}/{field_id}/observations?limit=10&offset={offset}"
        url_start_date = f"{self._weather_url}/{field_id}/observations/{start_day}"
        url_end_date = f"{self._weather_url}/{field_id}/observations/{end_day}"
        url_both_dates = f"{self._weather_url}/{field_id}/observations/{start_day},{end_day}?limit=10&offset={offset}"

        # Perform the HTTP request to obtain the norms for the Field
        # Default - 7-day
        if not (start_day or end_day):
            response = requests.get(url_no_date, headers=auth_headers)

        # Single date - specify start day
        elif start_day and not end_day:
            response = requests.get(url_start_date, headers=auth_headers)

        # Single date - specify end day
        elif end_day and not start_day:
            response = requests.get(url_end_date, headers=auth_headers)

        # Date range
        elif start_day and end_day:
            response = requests.get(url_both_dates, headers=auth_headers)

        # All other cases
        else:
            raise ValueError('Invalid parameters.')

        # Return the norms
        return response.json()

    def get_oauth_token(self, encoded_key_secret):
        """
        Demonstrates how to make a HTTP POST request to obtain an OAuth Token

        Docs:
            http://developer.awhere.com/api/authentication

        Returns:
            The access token provided by the aWhere API
        """
        # Define authorization parameters
        auth_url = 'https://api.awhere.com/oauth/token'

        auth_headers = {
            "Authorization": f"Basic {encoded_key_secret}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = "grant_type=client_credentials"

        # Perform HTTP request for OAuth Token
        response = requests.post(
            auth_url, headers=auth_headers, data=body)

        # Return access token
        return response.json()['access_token']
