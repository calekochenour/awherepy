import base64
import requests


class AWhereAPI():
    def __init__(self, api_key, api_secret):
        """
        Initializes the AWhereAPI class, which is used to perform HTTP requests
        to the aWhere V2 API.

        Docs:
            http://developer.awhere.com/api/reference
        """
        self._fields_url = 'https://api.awhere.com/v2/fields'
        self._weather_url = 'https://api.awhere.com/v2/weather/fields'
        """ Need to add in attributes for fields & plantings, agronomics, and models. There is a real opportunity to introduce goodness into this Python API class and methods."""
        # Plantings
        self._plantings_url = 'https://api.awhere.com/v2/agronomics/plantings'
        # Agronomics
        self._agronomics_url = 'https://api.awhere.com/v2/agronomics/fields'
        # Crops
        self._crops_url = 'https://api.awhere.com/v2/agronomics/fields/v2/agronomics/crops'
        # Models
        self._models_url = 'https://api.awhere.com//v2/agronomics/models'

        self.api_key = api_key
        self.api_secret = api_secret
        self.base_64_encoded_secret_key = self.encode_secret_and_key(
            self.api_key, self.api_secret)
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)
        # self._menu = Menus()  # Is this necessary if we are not going to use the terminal to work with the interface?

    """ Need function for create_field. Not test field. Relies on user input. """

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

        # Perform the POST request to create your Field
        print('Attempting to create new field....\n')
        response = requests.post(
            self._fields_url, headers=auth_headers, json=field_body)

        if response.status_code == 201:
            print(f"Your field {field_id} was successfully created!")
        else:
            print("An error occurred. Please review the above resonse and try again.")

        # Return the JSON formatted response
        # return response.json()
        # Need to return something - don't leave a function without a return

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
        # Perform the POST request to Delete your Field
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
        # print('\nKey and Secret before Base64 Encoding: %s' % key_secret)

        encoded_key_secret = base64.b64encode(
            bytes(key_secret, 'utf-8')).decode('ascii')

        # print('Key and Secret after Base64 Encoding: %s' % encoded_key_secret)
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

        # Display the count of Fields the user has on their account
        print(f"You have {len(responseJSON['fields'])} fields registered on your account")

        # Iterate over the fields and display their name and ID
        print('#  Field Name \t\t Field ID')
        print('-------------------------------------------')
        count = 0
        for field in responseJSON["fields"]:
            count += 1
            print(f"{count}. {field['name']} \t {field['id']}\r")

    def get_weather_by_id(self, field_id):
        """
        Performs a HTTP GET request to obtain Forecast, Historical Norms and Forecasts

        Docs:
            1. Forecast: http://developer.awhere.com/api/forecast-weather-api
            2. Historical Norms: http://developer.awhere.com/api/reference/weather/norms
            3. Observations: http://developer.awhere.com/api/reference/weather/observations
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the Forecast for the Field
        # Modify to include all parameters (optional, set as default values)
        response_forecast = requests.get(
            f"{self._weather_url}/{field_id}/forecasts?blockSize=24", headers=auth_headers)
        # return response.json()
        """pprint.pprint(response.json())
        print('\nThe above response from the Forecast API endpoint shows the forecast for your field location ({0}).'.format(
            field_id))"""
        # self._menu.os_pause()
        # return response.json()

        # Next, let's obtain the historic norms for a Field
        # Modify this so that user can supply a date in the correct format (mm-dd)

        # Historic norms for range of days - returns last 10 average
        # /v2/weather/fields/{fieldId}/norms/{startDay},{endDay}

        # Other options for more user flexibility
        # /v2/weather/fields/{fieldId}/norms/{month-day}/years/{startYear},{endYear}
        # /v2/weather/fields/{fieldId}/norms/{startDay},{endDay}/years/{startYear},{endYear}

        # Maxes at 10 days?

        response_historic_norms = requests.get(
            f"{self._weather_url}/{field_id}/norms/05-01,05-31", headers=auth_headers)
        """pprint.pprint(response.json())
        print('\nThe above response from the Norms API endpoint shows the averages of the last 10 for an arbitrary date, April 4th.')"""
        # self._menu.os_pause()

        # Finally, display the observed weather. Returns the last 7 days of data for the provided Field.
        # Add option to input other parameters?
        response_observed_7_day = requests.get(
            f"{self._weather_url}/{field_id}/observations",                                      headers=auth_headers)
        """pprint.pprint(response.json())
        print('\nThe above response from the Observed Weather API endpoint shows the last 7 days of data for the provided field ({0})'.format(
            field_id))"""

        # Return forecast, historic norms, previous 7 days
        return response_forecast.json(), response_historic_norms.json(), response_observed_7_day.json()

    def get_oauth_token(self, encoded_key_secret):
        """
        Demonstrates how to make a HTTP POST request to obtain an OAuth Token

        Docs:
            http://developer.awhere.com/api/authentication

        Returns:
            The access token provided by the aWhere API
        """
        auth_url = 'https://api.awhere.com/oauth/token'

        auth_headers = {
            "Authorization": f"Basic {encoded_key_secret}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        body = "grant_type=client_credentials"

        response = requests.post(auth_url,
                                 headers=auth_headers,
                                 data=body)

        # .json method is a requests lib method that decodes the response
        return response.json()['access_token']
