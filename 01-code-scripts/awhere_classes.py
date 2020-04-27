# Imports
# import os
import base64
import requests
from datetime import date
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd

""" BASE CLASS """


class AWhereAPI():
    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None, auth_token=None):
        # Define authorization information
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_64_encoded_secret_key = self.encode_secret_and_key(
            self.api_key, self.api_secret)
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)

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


""" FIELDS """


class Fields(AWhereAPI):
    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None, auth_token=None, api_url=None):
        super(Fields, self).__init__(api_key, api_secret,
                                     base_64_encoded_secret_key, auth_token)

        self.api_url = 'https://api.awhere.com/v2/fields'

    # Modify this to return all fields into a dataframe?
    def get(self, field_id=None, limit=10, offset=0):
        """
        Performs a HTTP GET request to obtain all Fields you've created on your aWhere App.

        Docs:
            http://developer.awhere.com/api/reference/fields/get-fields
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        if field_id:
            # Perform the HTTP request to obtain a specific field
            fields_response = requests.get(f"{self.api_url}/{field_id}", headers=auth_headers)

            message = fields_response.json()

        else:
            # Perform the HTTP request to obtain a list of all fields
            fields_response = requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)

            responseJSON = fields_response.json()

            # Display the count of Fields for the user account
            print(
                f"You have {len(responseJSON['fields'])} fields shown on this page.")

            # Iterate over the fields and display their name and ID
            print('#  Field Name \t\t Field ID')
            print('-------------------------------------------')
            count = 0
            for field in responseJSON["fields"]:
                count += 1
                print(f"{count}. {field['name']} \t {field['id']}\r")

            message = print("\nFields listed above.")

        return message

    def create(self, field_id, field_name, farm_id, center_latitude, center_longitude, acres):
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
            self.api_url, headers=auth_headers, json=field_body)

        return response.json()

    def update(self, field_id, name=None, farm_id=None):
        """Update the name and/or farm id for a field.
        """
        if not (name or farm_id):
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }, {
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        elif name and not farm_id:
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }]

        elif farm_id and not name:
            field_body = [{
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        elif name and farm_id:
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }, {
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
        }

        # Perform the HTTP request to update field information
        response = requests.patch(
            f"{self.api_url}/{field_id}", headers=auth_headers, json=field_body)

        return response.json()

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
            "Content-Type": 'application/json'
        }

        # Perform the POST request to Delete the Field
        response = requests.delete(
            f"{self.api_url}/{field_id}", headers=auth_headers)

        message = f"Deleted field: {field_id}" if response.status_code == 204 else f"Could not delete field."

        return print(message)


class Field(Fields):
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None, auth_token=None, api_url=None):
        super(Field, self).__init__(api_key, api_secret,
                                    base_64_encoded_secret_key, auth_token)

        self.field_id = field_id
        self.api_url = f'https://api.awhere.com/v2/fields/{self.field_id}'

    def get(self):
        """
        Performs a HTTP GET request to obtain all Fields you've created on your aWhere App.

        Docs:
            http://developer.awhere.com/api/reference/fields/get-fields
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the field information
        field_response = requests.get(f"{self.api_url}",
                                      headers=auth_headers)

        #responseJSON = fields_response.json()

        return field_response.json()

    def create(self):
        pass

    def update(self, name=None, farm_id=None):
        """Update the name and/or farm id for a field.
        """
        if not (name or farm_id):
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }, {
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        elif name and not farm_id:
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }]

        elif farm_id and not name:
            field_body = [{
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        elif name and farm_id:
            field_body = [{
                "op": "replace",
                "path": "/name",
                "value": name
            }, {
                "op": "replace",
                "path": "/farmId",
                "value": farm_id
            }]

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
        }

        # Perform the HTTP request to update field information
        response = requests.patch(
            f"{self.api_url}", headers=auth_headers, json=field_body)

        return response.json()

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
            "Content-Type": 'application/json'
        }

        # Perform the POST request to Delete the Field
        response = requests.delete(f"{self.api_url}", headers=auth_headers)

        message = f"Deleted field: {self.field_id}" if response.status_code == 204 else f"Could not delete field."

        return print(message)


""" WEATHER """


class Weather(AWhereAPI):
    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None, auth_token=None, api_url=None):
        super(Weather, self).__init__(api_key, api_secret,
                                      base_64_encoded_secret_key, auth_token)

        self.api_url = 'https://api.awhere.com/v2/weather'

    @staticmethod
    def get_data():
        pass

    @staticmethod
    def extract_data():
        pass

    @staticmethod
    def clean_data(df, lon_lat_cols, drop_cols, name_map):
        """Converts dataframe to geodataframe,
        drops unnecessary columns, and renames
        columns.

        Parameters
        ----------
        df : dataframe
            Input dataframe.

        lon_lat_cols : list
            List containing the column name for longitude (list[0])
            and latitude (list[1]) attributes.

        drop_cols : list (of str)
            List of column names to be dropped.

        name_map : dict
            Dictionaty mapping old columns names (keys)
            to new column names (values).

        Returns
        -------
        gdf : geodataframe
            Cleaned geodataframe.

        Example
        -------
        """
        # Define CRS (EPSG 4326) - make this a parameter?
        crs = {'init': 'epsg:4326'}

        # Rename index - possibly as option, or take care of index prior?
        #df.index.rename('date_rename', inplace=True)

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy, crs=crs, geometry=gpd.points_from_xy(
                df[lon_lat_cols[0]],
                df[lon_lat_cols[1]])
        )

        # Add lat/lon columns to drop columns list
        drop_cols += lon_lat_cols

        # Drop columns
        gdf.drop(columns=drop_cols, axis=1, inplace=True)

        # Rename columns
        gdf.rename(columns=name_map, inplace=True)

        # Return cleaned up geodataframe
        return gdf

    @classmethod
    def api_to_gdf(cls, api_object, kwargs=None):
        """kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        api_data_df = cls.extract_data(api_data_json)

        api_data_gdf = cls.clean_data(
            api_data_df,
            cls.coord_cols,
            cls.drop_cols,
            cls.rename_map
        )

        return api_data_gdf


class WeatherLocation(Weather):
    def __init__(self, api_key, api_secret,
                 base_64_encoded_secret_key=None, auth_token=None, api_url=None):

        super(WeatherLocation, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.api_url = f"{self.api_url}/locations"


class WeatherField(Weather):
    def __init__(self, api_key, api_secret,
                 base_64_encoded_secret_key=None, auth_token=None, api_url=None):

        super(WeatherField, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.api_url = f"{self.api_url}/fields"


class WeatherLocationNorms(WeatherLocation):
    # Class variables for clean_data() function
    coord_cols = ['location.longitude', 'location.latitude']

    drop_cols = [
        'meanTemp.units', 'maxTemp.units',
        'minTemp.units', 'precipitation.units', 'solar.units',
        'dailyMaxWind.units', 'averageWind.units'
    ]

    rename_map = {
        'meanTemp.average': 'mean_temp_avg_cels',
        'meanTemp.stdDev': 'mean_temp_std_dev_cels',
        'maxTemp.average': 'max_temp_avg_cels',
        'maxTemp.stdDev': 'max_temp_std_dev_cels',
        'minTemp.average': 'min_temp_avg_cels',
        'minTemp.stdDev': 'min_temp_std_dev_cels',
        'precipitation.average': 'precip_avg_mm',
        'precipitation.stdDev': 'precip_std_dev_mm',
        'solar.average': 'solar_avg_w_h_per_m2',
        'solar.stdDev': 'solar_avg_std_dev_w_h_per_m2',
        'minHumidity.average': 'min_humiduty_avg_%',
        'minHumidity.stdDev': 'min_humidity_std_dev_%',
        'maxHumidity.average': 'max_humiduty_avg_%',
        'maxHumidity.stdDev': 'max_humidity_std_dev_%',
        'dailyMaxWind.average': 'daily_max_wind_avg_m_per_sec',
        'dailyMaxWind.stdDev': 'daily_max_wind_std_dev_m_per_sec',
        'averageWind.average': 'average_wind_m_per_sec',
        'averageWind.stdDev': 'average_wind_std_dev_m_per_sec'
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, latitude, longitude, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(WeatherLocationNorms, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/norms"

    def get_data(self, start_day='01-01', end_day=None, offset=0):
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
        url_single_day = f"{self.api_url}/{start_day}?limit=10&offset={offset}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(historic_norms):
        """Creates a dataframe from a JSON-like
        dictionary of aWhere historic norm data.

        Handles both single-day norms and multiple days.

        Parameters
        ----------
        historic_norms : dict
            aWhere historic norm data in dictionary format.

        Returns
        -------
        historic_norms_df : pandas dataframe
            Flattened dataframe version of historic norms.
        """
        # Check if multiple entries (days) are in norms
        if historic_norms.get('norms'):
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms.get('norms'))

        # Single-day norm
        else:
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms)

        # Set day as index
        historic_norms_df.set_index('day', inplace=True)

        # Drop unnecessary columns
        historic_norms_df.drop(
            columns=['_links.self.href'],
            axis=1, inplace=True)

        # Return dataframe
        return historic_norms_df


class WeatherLocationObserved(WeatherLocation):
    # Class variables for clean_data() function
    coord_cols = ['location.longitude', 'location.latitude']

    drop_cols = [
        'temperatures.units', 'precipitation.units',
        'solar.units', 'wind.units'
    ]

    rename_map = {
        'temperatures.max': 'temp_max_cels',
        'temperatures.min': 'temp_min_cels',
        'precipitation.amount': 'precip_amount_mm',
        'solar.amount': 'solar_energy_w_h_per_m2',
        'relativeHumidity.average': 'rel_humidity_avg_%',
        'relativeHumidity.max': 'rel_humidity_max_%',
        'relativeHumidity.min': 'rel_humidity_min_%',
        'wind.morningMax': 'wind_morning_max_m_per_sec',
        'wind.dayMax': 'wind_day_max_m_per_sec',
        'wind.average': 'wind_avg_m_per_sec',
    }

    def __init__(self, api_key, api_secret, latitude, longitude,
                 base_64_encoded_secret_key=None, auth_token=None, api_url=None):

        super(WeatherLocationObserved, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/observations"

    def get_data(self, start_day=None, end_day=None, offset=0):
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
        url_no_date = f"{self.api_url}?limit=10&offset={offset}"
        url_start_date = f"{self.api_url}/{start_day}"
        url_end_date = f"{self.api_url}/{end_day}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

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

        # Return the observed
        return response.json()

    @staticmethod
    def extract_data(observed_weather):
        """Creates a dataframe from a JSON-like
        dictionary of aWhere observed weather data.

        Parameters
        ----------
        observed_weather : dict
            aWhere historic norm data in dictionary format.

        Returns
        -------
        observed_weather_df : pandas dataframe
            Flattened dataframe version of historic norms.
        """
        # Check if multiple entries (days) are in observed
        if observed_weather.get('observations'):
            # Flatten to dataframe
            observed_weather_df = json_normalize(
                observed_weather.get('observations'))

        # Single-day observed
        else:
            # Flatten to dataframe
            observed_weather_df = json_normalize(observed_weather)

        # Set date as index
        observed_weather_df.set_index('date', inplace=True)

        # Drop unnecessary columns
        observed_weather_df.drop(
            columns=['_links.self.href'],
            axis=1, inplace=True)

        # Return dataframe
        return observed_weather_df


class WeatherLocationForecast(WeatherLocation):
    # Class variables for clean_data() function
    # Main forecast
    coord_cols = ['longitude', 'latitude']

    drop_cols = [
        'temperatures.units', 'precipitation.units',
        'solar.units', 'wind.units', 'dewPoint.units'
    ]

    rename_map = {
        'startTime': 'start_time',
        'endTime': 'end_time',
        'conditionsCode': 'conditions_code',
        'conditionsText': 'conditions_text',
        'temperatures.max': 'temp_max_cels',
        'temperatures.min': 'temp_min_cels',
        'precipitation.chance': 'precip_chance_%',
        'precipitation.amount': 'precip_amount_mm',
        'sky.cloudCover': 'sky_cloud_cover_%',
        'sky.sunshine': 'sky_sunshine_%',
        'solar.amount': 'solar_energy_w_h_per_m2',
        'relativeHumidity.average': 'rel_humidity_avg_%',
        'relativeHumidity.max': 'rel_humidity_max_%',
        'relativeHumidity.min': 'rel_humidity_min_%',
        'wind.average': 'wind_avg_m_per_sec',
        'wind.max': 'wind_max_m_per_sec',
        'wind.min': 'wind_min_m_per_sec',
        'wind.bearing': 'wind_bearing_deg',
        'wind.direction': 'wind_direction_compass',
        'dewPoint.amount': 'dew_point_cels'
    }

    # Soil
    soil_coord_cols = ['longitude', 'latitude']

    soil_drop_cols = ['units']

    soil_rename_map = {
        'average_temp': 'soil_temp_avg_cels',
        'max_temp': 'soil_temp_max_cels',
        'min_temp': 'soil_temp_min_cels',
        'average_moisture': 'soil_moisture_avg_%',
        'max_moisture': 'soil_moisture_max_%',
        'min_moisture': 'soil_moisture_min_%',
    }

    def __init__(self, api_key, api_secret, latitude, longitude, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(WeatherLocationForecast, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/forecasts"

    def get_data(self, start_day=None, end_day=None, offset=0, block_size=24):
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

        # Define URL variants
        url_no_date = f"{self.api_url}?limit=10&offset={offset}&blockSize={block_size}"
        url_start_date = f"{self.api_url}/{start_day}?limit=10&offset={offset}&blockSize={block_size}"
        url_end_date = f"{self.api_url}/{end_day}?limit=10&offset={offset}&blockSize={block_size}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}&blockSize={block_size}"

        # Perform the HTTP request to obtain the Forecast for the Field
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

        # Return forecast
        return response.json()

    @staticmethod
    def extract_data(forecast):
        """Extract aWhere forecast data and returns
        it in a pandas dataframe.
        """
        # Initialize lists to store forecast
        forecast_main_list = []

        # Check if more than one day
        if forecast.get('forecasts'):
            forecast_iterator = json_normalize(forecast.get('forecasts'))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level dataframe outputs
            date = row['date']
            lat = row['location.latitude']
            lon = row['location.longitude']

            # Extract the main forecast from the top-level dataframe
            forecast = row['forecast']

            # Faltten data into dataframe
            forecast_norm = json_normalize(forecast)

            # Drop soil moisture and soil temperature columns
            #  (will be extracted as indivdiual dataframes)
            forecast_norm.drop(columns=[
                'soilTemperatures',
                'soilMoisture',
            ],
                axis=1, inplace=True)
            # Assign date, lat/lon to dataframe
            forecast_norm['date'] = date
            forecast_norm['latitude'] = lat
            forecast_norm['longitude'] = lon

            # Set date as index
            forecast_norm.set_index(['date'], inplace=True)

            # Add the dataframe to a list of dataframes
            forecast_main_list.append(forecast_norm)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_main_list)

    @staticmethod
    def extract_soil(forecast):
        """Extract aWhere forecast soil
        data and returns it in a pandas dataframe.
        """
        # Initialize lists to store soil dataframes
        forecast_soil_list = []

        # Check if more than one day
        if forecast.get('forecasts'):
            forecast_iterator = json_normalize(forecast.get('forecasts'))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level dataframe outputs
            date = row['date']
            lat = row['location.latitude']
            lon = row['location.longitude']

            # Get soil temperature data
            forecast_soil_temp = row['forecast'][0].get('soilTemperatures')
            forecast_soil_moisture = row['forecast'][0].get('soilMoisture')

            # Flatten data into dataframe
            forecast_soil_temp_df = json_normalize(forecast_soil_temp)
            forecast_soil_moisture_df = json_normalize(forecast_soil_moisture)

            # Combine temperature and moisture
            forecast_soil_df = forecast_soil_temp_df.merge(
                forecast_soil_moisture_df, on='depth', suffixes=('_temp', '_moisture'))

            # Assign date, lat/lon to dataframe
            forecast_soil_df['date'] = date
            forecast_soil_df['latitude'] = lat
            forecast_soil_df['longitude'] = lon

            # Shorten depth values to numerics (will be used in MultiIndex)
            forecast_soil_df['depth'] = forecast_soil_df['depth'].apply(
                lambda x: x[0:-15])

            # Rename depth prior to indexing
            forecast_soil_df.rename(
                columns={'depth': 'ground_depth_m'}, inplace=True)

            # Create multi-index dataframe for date and soil depth (rename depth columns? rather long)
            soil_multi_index = forecast_soil_df.set_index(
                ['date', 'ground_depth_m'])

            # Add dataframe to list of dataframes
            forecast_soil_list.append(soil_multi_index)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_soil_list)

    @classmethod
    def api_to_gdf(cls, api_object, forecast_type='main', kwargs=None):
        """
        forecast_type can either be 'main' or 'soil'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if forecast_type.lower() == 'main':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.coord_cols,
                cls.drop_cols,
                cls.rename_map
            )

        elif forecast_type.lower() == 'soil':
            api_data_df = cls.extract_soil(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.soil_coord_cols,
                cls.soil_drop_cols,
                cls.soil_rename_map
            )

        else:
            raise ValueError("Invalid forecast type. Please choose 'main' or 'soil'.")

        return api_data_gdf


class WeatherFieldNorms(WeatherField):
    # Class variables for clean_data() function
    coord_cols = ['location.longitude', 'location.latitude']

    drop_cols = [
        'location.fieldId', 'meanTemp.units', 'maxTemp.units',
        'minTemp.units', 'precipitation.units', 'solar.units',
        'dailyMaxWind.units', 'averageWind.units'
    ]

    rename_map = {
        'meanTemp.average': 'mean_temp_avg_cels',
        'meanTemp.stdDev': 'mean_temp_std_dev_cels',
        'maxTemp.average': 'max_temp_avg_cels',
        'maxTemp.stdDev': 'max_temp_std_dev_cels',
        'minTemp.average': 'min_temp_avg_cels',
        'minTemp.stdDev': 'min_temp_std_dev_cels',
        'precipitation.average': 'precip_avg_mm',
        'precipitation.stdDev': 'precip_std_dev_mm',
        'solar.average': 'solar_avg_w_h_per_m2',
        'minHumidity.average': 'min_humiduty_avg_%',
        'minHumidity.stdDev': 'min_humidity_std_dev_%',
        'maxHumidity.average': 'max_humiduty_avg_%',
        'maxHumidity.stdDev': 'max_humidity_std_dev_%',
        'dailyMaxWind.average': 'daily_max_wind_avg_m_per_sec',
        'dailyMaxWind.stdDev': 'daily_max_wind_std_dev_m_per_sec',
        'averageWind.average': 'average_wind_m_per_sec',
        'averageWind.stdDev': 'average_wind_std_dev_m_per_sec'
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(WeatherFieldNorms, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/norms"

    def get_data(self, start_day='01-01', end_day=None, offset=0):
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
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}?limit=10&offset={offset}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(historic_norms):
        """Creates a dataframe from a JSON-like
        dictionary of aWhere historic norm data.

        Handles both single-day norms and multiple days.

        Parameters
        ----------
        historic_norms : dict
            aWhere historic norm data in dictionary format.

        Returns
        -------
        historic_norms_df : pandas dataframe
            Flattened dataframe version of historic norms.
        """
        # Check if multiple entries (days) are in norms
        if historic_norms.get('norms'):
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms.get('norms'))

        # Single-day norm
        else:
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms)

        # Set day as index
        historic_norms_df.set_index('day', inplace=True)

        # Drop unnecessary columns
        historic_norms_df.drop(
            columns=[
                '_links.self.href',
                '_links.curies',
                '_links.awhere:field.href'],
            axis=1, inplace=True)

        # Return dataframe
        return historic_norms_df


class WeatherFieldObserved(WeatherField):
    # Class variables for clean_data() function
    coord_cols = ['location.longitude', 'location.latitude']

    drop_cols = [
        'location.fieldId', 'temperatures.units', 'precipitation.units',
        'solar.units', 'wind.units'
    ]

    rename_map = {
        'temperatures.max': 'temp_max_cels',
        'temperatures.min': 'temp_min_cels',
        'precipitation.amount': 'precip_amount_mm',
        'solar.amount': 'solar_energy_w_h_per_m2',
        'relativeHumidity.average': 'rel_humidity_avg_%',
        'relativeHumidity.max': 'rel_humidity_max_%',
        'relativeHumidity.min': 'rel_humidity_min_%',
        'wind.morningMax': 'wind_morning_max_m_per_sec',
        'wind.dayMax': 'wind_day_max_m_per_sec',
        'wind.average': 'wind_avg_m_per_sec',
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(WeatherFieldObserved, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/observations"

    def get_data(self, start_day=None, end_day=None, offset=0):
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
        url_no_date = f"{self.api_url}?limit=10&offset={offset}"
        url_start_date = f"{self.api_url}/{start_day}"
        url_end_date = f"{self.api_url}/{end_day}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

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

        # Return the observed
        return response.json()

    @staticmethod
    def extract_data(observed_weather):
        """Creates a dataframe from a JSON-like
        dictionary of aWhere observed weather data.

        Parameters
        ----------
        observed_weather : dict
            aWhere historic norm data in dictionary format.

        Returns
        -------
        observed_weather_df : pandas dataframe
            Flattened dataframe version of historic norms.
        """
        # Check if multiple entries (days) are in observed
        if observed_weather.get('observations'):
            # Flatten to dataframe
            observed_weather_df = json_normalize(observed_weather.get('observations'))

        # Single-day observed
        else:
            # Flatten to dataframe
            observed_weather_df = json_normalize(observed_weather)

        # Set date as index
        observed_weather_df.set_index('date', inplace=True)

        # Drop unnecessary columns
        observed_weather_df.drop(
            columns=[
                '_links.self.href',
                '_links.curies',
                '_links.awhere:field.href'],
            axis=1, inplace=True)

        # Return dataframe
        return observed_weather_df


class WeatherFieldForecast(WeatherField):
    # Class variables for clean_data() function
    # Main forecast
    coord_cols = ['longitude', 'latitude']

    drop_cols = [
        'temperatures.units', 'precipitation.units',
        'solar.units', 'wind.units', 'dewPoint.units'
    ]

    rename_map = {
        'startTime': 'start_time',
        'endTime': 'end_time',
        'conditionsCode': 'conditions_code',
        'conditionsText': 'conditions_text',
        'temperatures.max': 'temp_max_cels',
        'temperatures.min': 'temp_min_cels',
        'precipitation.chance': 'precip_chance_%',
        'precipitation.amount': 'precip_amount_mm',
        'sky.cloudCover': 'sky_cloud_cover_%',
        'sky.sunshine': 'sky_sunshine_%',
        'solar.amount': 'solar_energy_w_h_per_m2',
        'relativeHumidity.average': 'rel_humidity_avg_%',
        'relativeHumidity.max': 'rel_humidity_max_%',
        'relativeHumidity.min': 'rel_humidity_min_%',
        'wind.average': 'wind_avg_m_per_sec',
        'wind.max': 'wind_max_m_per_sec',
        'wind.min': 'wind_min_m_per_sec',
        'wind.bearing': 'wind_bearing_deg',
        'wind.direction': 'wind_direction_compass',
        'dewPoint.amount': 'dew_point_cels'
    }

    # Soil
    soil_coord_cols = ['longitude', 'latitude']

    soil_drop_cols = ['units']

    soil_rename_map = {
        'average_temp': 'soil_temp_avg_cels',
        'max_temp': 'soil_temp_max_cels',
        'min_temp': 'soil_temp_min_cels',
        'average_moisture': 'soil_moisture_avg_%',
        'max_moisture': 'soil_moisture_max_%',
        'min_moisture': 'soil_moisture_min_%',
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(WeatherFieldForecast, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/forecasts"

    def get_data(self, start_day=None, end_day=None, offset=0, block_size=24):
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

        # Define URL variants
        url_no_date = f"{self.api_url}?limit=10&offset={offset}&blockSize={block_size}"
        url_start_date = f"{self.api_url}/{start_day}?limit=10&offset={offset}&blockSize={block_size}"
        url_end_date = f"{self.api_url}/{end_day}?limit=10&offset={offset}&blockSize={block_size}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}&blockSize={block_size}"

        # Perform the HTTP request to obtain the Forecast for the Field
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

        # Return forecast
        return response.json()

    @staticmethod
    def extract_data(forecast):
        """Extract aWhere forecast data and returns
        it in a pandas dataframe.
        """
        # Initialize lists to store forecast
        forecast_main_list = []

        # Check if more than one day
        if forecast.get('forecasts'):
            forecast_iterator = json_normalize(forecast.get('forecasts'))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level dataframe outputs
            date = row['date']
            lat = row['location.latitude']
            lon = row['location.longitude']

            # Extract the main forecast from the top-level dataframe
            forecast = row['forecast']

            # Faltten data into dataframe
            forecast_norm = json_normalize(forecast)

            # Drop soil moisture and soil temperature columns
            #  (will be extracted as indivdiual dataframes)
            forecast_norm.drop(columns=[
                'soilTemperatures',
                'soilMoisture',
            ],
                axis=1, inplace=True)

            # Assign date, lat/lon to dataframe
            forecast_norm['date'] = date
            forecast_norm['latitude'] = lat
            forecast_norm['longitude'] = lon

            # Set date as index
            forecast_norm.set_index(['date'], inplace=True)

            # Add the dataframe to a list of dataframes
            forecast_main_list.append(forecast_norm)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_main_list)

    @staticmethod
    def extract_soil(forecast):
        """Extract aWhere forecast soil
        data and returns it in a pandas dataframe.
        """
        # Initialize lists to store soil dataframes
        forecast_soil_list = []

        # Check if more than one day
        if forecast.get('forecasts'):
            forecast_iterator = json_normalize(forecast.get('forecasts'))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level dataframe outputs
            date = row['date']
            lat = row['location.latitude']
            lon = row['location.longitude']

            # Get soil temperature data
            forecast_soil_temp = row['forecast'][0].get('soilTemperatures')
            forecast_soil_moisture = row['forecast'][0].get('soilMoisture')

            # Flatten data into dataframe
            forecast_soil_temp_df = json_normalize(forecast_soil_temp)
            forecast_soil_moisture_df = json_normalize(forecast_soil_moisture)

            # Combine temperature and moisture
            forecast_soil_df = forecast_soil_temp_df.merge(
                forecast_soil_moisture_df, on='depth', suffixes=('_temp', '_moisture'))

            # Assign date, lat/lon to dataframe
            forecast_soil_df['date'] = date
            forecast_soil_df['latitude'] = lat
            forecast_soil_df['longitude'] = lon

            # Shorten depth values to numerics (will be used in MultiIndex)
            forecast_soil_df['depth'] = forecast_soil_df['depth'].apply(lambda x: x[0:-15])

            # Rename depth prior to indexing
            forecast_soil_df.rename(columns={'depth': 'ground_depth_m'}, inplace=True)

            # Create multi-index dataframe for date and soil depth (rename depth columns? rather long)
            soil_multi_index = forecast_soil_df.set_index(
                ['date', 'ground_depth_m'])

            # Add dataframe to list of dataframes
            forecast_soil_list.append(soil_multi_index)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_soil_list)

    @classmethod
    def api_to_gdf(cls, api_object, forecast_type='main', kwargs=None):
        """
        forecast_type can either be 'main' or 'soil'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if forecast_type.lower() == 'main':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.coord_cols,
                cls.drop_cols,
                cls.rename_map
            )

        elif forecast_type.lower() == 'soil':
            api_data_df = cls.extract_soil(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.soil_coord_cols,
                cls.soil_drop_cols,
                cls.soil_rename_map
            )

        else:
            raise ValueError("Invalid forecast type. Please choose 'main' or 'soil'.")

        return api_data_gdf


""" AGRONOMICS """


class Agronomics(AWhereAPI):
    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None, auth_token=None, api_url=None):
        super(Agronomics, self).__init__(api_key, api_secret,
                                         base_64_encoded_secret_key, auth_token)

        self.api_url = 'https://api.awhere.com/v2/agronomics'

    def get_data():
        pass

    @staticmethod
    def extract_data():
        pass

    @staticmethod
    def clean_data(df, lon_lat_cols, drop_cols, name_map):
        """Converts dataframe to geodataframe,
        drops unnecessary columns, and renames
        columns.

        Parameters
        ----------
        df : dataframe
            Input dataframe.

        lon_lat_cols : list
            List containing the column name for longitude (list[0])
            and latitude (list[1]) attributes.

        drop_cols : list (of str)
            List of column names to be dropped.

        name_map : dict
            Dictionaty mapping old columns names (keys)
            to new column names (values).

        Returns
        -------
        gdf : geodataframe
            Cleaned geodataframe.

        Example
        -------
        """
        # Define CRS (EPSG 4326) - make this a parameter?
        crs = {'init': 'epsg:4326'}

        # Rename index - possibly as option, or take care of index prior?
        #df.index.rename('date_rename', inplace=True)

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy, crs=crs, geometry=gpd.points_from_xy(
                df[lon_lat_cols[0]],
                df[lon_lat_cols[1]])
        )

        # Add lat/lon columns to drop columns list
        drop_cols += lon_lat_cols

        # Drop columns
        gdf.drop(columns=drop_cols, axis=1, inplace=True)

        # Rename columns
        gdf.rename(columns=name_map, inplace=True)

        # Return cleaned up geodataframe
        return gdf

    @classmethod
    def api_to_gdf(cls, api_object, kwargs=None):
        """kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        api_data_df = cls.extract_data(api_data_json)

        api_data_gdf = cls.clean_data(
            api_data_df,
            cls.coord_cols,
            cls.drop_cols,
            cls.rename_map
        )

        return api_data_gdf


class AgronomicsLocation(Agronomics):

    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsLocation, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token)

        self.api_url = f"{self.api_url}/locations"


class AgronomicsField(Agronomics):

    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsField, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token)

        self.api_url = f"{self.api_url}/fields"


class AgronomicsLocationValues(AgronomicsLocation):

    # Class variables for clean_data() function
    # Single day
    day_coord_cols = ['location.longitude', 'location.latitude']

    day_drop_cols = ['pet.units', '_links.self.href']

    day_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "pet.amount": "pet_daily_total_mm"
    }

    # Multi-day, total accumulation
    total_coord_cols = ['longitude', 'latitude']

    total_drop_cols = ['precipitation.units', 'pet.units']

    total_rename_map = {  # PPET overall?? Range total
        "gdd": "gdd_range_total_cels",
        "ppet": "ppet_range_total",  # This is accumulation of all daily PPET
        "precipitation.amount": "precip_range_total_mm",
        "pet.amount": "pet_range_total_mm"
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ['longitude', 'latitude']

    daily_drop_cols = ['pet.units', 'accumulatedPrecipitation.units',
                       'accumulatedPet.units', '_links.self.href']

    daily_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "accumulatedGdd": "gdd_rolling_total_cels",
        "accumulatedPpet": "ppet_rolling_total",
        "pet.amount": "pet_daily_total_mm",
        "accumulatedPrecipitation.amount": "precip_rolling_total_mm",
        "accumulatedPet.amount": "pet_rolling_total_mm"
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, latitude, longitude, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsLocationValues, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/agronomicvalues"

    def get_data(self, start_day=date.today().strftime("%m-%d"), end_day=None, offset=0):
        """Returns aWhere Forecast Agronomic Values.
        """

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_values):
        """Extracts data from the aWhere agronomic forecast
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_values.get('location').get('latitude')
        longitude = agronomic_values.get('location').get('longitude')

        # Check if more than one day
        if agronomic_values.get('dailyValues'):

            # Do these with a separate call, just like in Soil accumulation='daily'
            #  accumulation='total'

            # DAILY ACCUMULATIONS
            # Get daily forecasted accumulations
            daily_accumulation = json_normalize(
                agronomic_values.get('dailyValues'))

            # Add lat/lon and set date as index
            daily_accumulation['latitude'] = latitude
            daily_accumulation['longitude'] = longitude
            daily_accumulation.set_index(['date'], inplace=True)

            # TOTAL ACCUMULATION
            # Get total forecasted accumulations through all days
            total_accumulation = json_normalize(
                agronomic_values.get('accumulations'))

            # Get list of dates, add start/end dates, set date range as index
            dates = [entry.get('date')
                     for entry in agronomic_values.get('dailyValues')]
            total_accumulation['date_range'] = f"{dates[0]}/{dates[-1]}"
            total_accumulation['start_day'] = dates[0]
            total_accumulation['end_day'] = dates[-1]
            total_accumulation.set_index(['date_range'], inplace=True)

            # Add lat/lon
            total_accumulation['latitude'] = latitude
            total_accumulation['longitude'] = longitude

            # Put dataframes in tuple (total accumulation, daily accumulation)
            agronomics_df = (total_accumulation, daily_accumulation)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_values)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(['date'], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type='single_day', kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if value_type.lower() == 'single_day':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map
            )

        elif value_type.lower() == 'multi_day':
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json)

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError("Invalid value type. Please choose 'single_day' or 'multi_day'.")

        return api_data_gdf


class AgronomicsLocationNorms(AgronomicsLocation):

    # Class variables for clean_data() function

    # https://developer.awhere.com/api/reference/agronomics/norms/geolocation

    """The average ratio of Precipitation to Potential Evapotranspiration
    over the years specified. When this value is above 1, then more rain fell
    than the amount of likely water loss; if it's below 1, then more water was
    likely lost than fell as rain. P/PET is most useful when calculated for a
    range of days, as it is for this property, than for individual days."""

    # Single day
    day_coord_cols = ['location.longitude', 'location.latitude']

    day_drop_cols = ['pet.units', '_links.self.href']

    day_rename_map = {
        "gdd.average": "gdd_daily_average_total_cels",
        "gdd.stdDev": "gdd_daily_average_total_std_dev_cels",
        "pet.average": "pet_daily_average_total_mm",
        "pet.stdDev": "pet_daily_average_total_std_dev_mm",
        "ppet.average": "ppet_daily_average_total",
        "ppet.stdDev": "ppet_daily_average_total_std_dev"
    }

    # Multi-day, total accumulation
    total_coord_cols = ['longitude', 'latitude']

    total_drop_cols = ['precipitation.units', 'pet.units']

    total_rename_map = {
        "gdd.average": "norms_gdd_average_total_cels",
        "gdd.stdDev": "norms_gdd_average_total_std_dev_cels",
        "precipitation.average": "norms_precip_average_total_mm",
        "precipitation.stdDev": "norms_precip_average_total_std_dev_mm",
        "pet.average": "norms_pet_average_total_mm",
        "pet.stdDev": "norms_pet_average_total_std_dev",
        "ppet.average": "norms_ppet_average_total",
        "ppet.stdDev": "norms_ppet_average_total_std_dev"
    }

    total_rename_map = {
        "gdd.average": "gdd_range_average_total_cels",
        "gdd.stdDev": "gdd_range_average_total_std_dev_cels",
        "precipitation.average": "precip_range_average_total_mm",
        "precipitation.stdDev": "precip_range_average_total_std_dev_mm",
        "pet.average": "pet_range_average_total_mm",
        "pet.stdDev": "pet_range_average_total_std_dev",
        # Why doesn't this match with precip_avg/pet_avg?
        # What causes this difference?
        # Is it the average of each of individual PPET daily values?
        # Seems like it
        "ppet.average": "ppet_range_daily_average",
        "ppet.stdDev": "ppet_range_daily_average_std_dev"
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ['longitude', 'latitude']

    daily_drop_cols = ['pet.units', 'accumulatedPrecipitation.units',
                       'accumulatedPet.units', '_links.self.href']

    daily_rename_map = {
        "gdd.average": "gdd_daily_average_cels",
        "gdd.stdDev": "gdd_daily_average_std_dev_cels",
        "pet.average": "pet_daily_average_mm",
        "pet.stdDev": "pet_daily_average_std_dev_mm",
        "ppet.average": "ppet_daliy_average",
        "ppet.stdDev": "ppet_daily_average_std_dev",
        "accumulatedGdd.average": "gdd_rolling_total_average",
        "accumulatedGdd.stdDev": "gdd_rolling_total_average_std_dev",
        "accumulatedPrecipitation.average": "precip_rolling_total_average_mm",
        "accumulatedPrecipitation.stdDev": "precip_rolling_total_average_std_dev_mm",
        "accumulatedPet.average": "pet_rolling_total_average_mm",
        "accumulatedPet.stdDev": "pet_rolling_total_average_std_dev_mm",
        "accumulatedPpet.average": "ppet_rolling_total_average",
        "accumulatedPpet.stdDev": "ppet_rolling_total_average_std_dev"
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, latitude, longitude, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsLocationNorms, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/agronomicnorms"

    def get_data(self, start_day='01-01', end_day=None, offset=0):
        """Returns aWhere Historic Agronomic Norms.
        """

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_norms):
        """Extracts data from the aWhere agronomic norms
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_norms.get('location').get('latitude')
        longitude = agronomic_norms.get('location').get('longitude')

        # Check if more than one day
        if agronomic_norms.get('dailyNorms'):

            # DAILY ACCUMULATION NORMS
            # Get daily accumulation norms
            daily_norms = json_normalize(
                agronomic_norms.get('dailyNorms'))

            # Add lat/lon and set date as index
            daily_norms['latitude'] = latitude
            daily_norms['longitude'] = longitude
            daily_norms.set_index(['day'], inplace=True)

            # TOTAL ACCUMULATION NORMS
            # Get average accumulations through all days
            total_norms = json_normalize(
                agronomic_norms.get('averageAccumulations'))

            # Get list of dates, add start/end dates, set date range as index
            dates = [entry.get('day')
                     for entry in agronomic_norms.get('dailyNorms')]
            total_norms['date_range'] = f"{dates[0]}/{dates[-1]}"
            total_norms['start_day'] = dates[0]
            total_norms['end_day'] = dates[-1]
            total_norms.set_index(['date_range'], inplace=True)

            # Add lat/lon
            total_norms['latitude'] = latitude
            total_norms['longitude'] = longitude

            # Put dataframes in tuple (total norms, daily norms)
            agronomics_df = (total_norms, daily_norms)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_norms)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(['day'], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type='single_day', kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if value_type.lower() == 'single_day':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map
            )

        elif value_type.lower() == 'multi_day':
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json)

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError("Invalid value type. Please choose 'single_day' or 'multi_day'.")

        return api_data_gdf


class AgronomicsFieldValues(AgronomicsField):

    # Class variables for clean_data() function
    # Single day
    day_coord_cols = ['location.longitude', 'location.latitude']

    day_drop_cols = ['location.fieldId', 'pet.units', '_links.self.href',
                     '_links.curies', '_links.awhere:field.href']

    day_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "pet.amount": "pet_daily_total_mm"
    }

    # Multi-day, total accumulation
    total_coord_cols = ['longitude', 'latitude']

    total_drop_cols = ['precipitation.units', 'pet.units']

    total_rename_map = {  # PPET overall?? Range total
        "gdd": "gdd_range_total_cels",
        "ppet": "ppet_range_total",  # This is accumulation of all daily PPET
        "precipitation.amount": "precip_range_total_mm",
        "pet.amount": "pet_range_total_mm"
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ['longitude', 'latitude']

    daily_drop_cols = ['pet.units', 'accumulatedPrecipitation.units',
                       'accumulatedPet.units', '_links.self.href',
                       '_links.curies', '_links.awhere:field.href']

    daily_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "accumulatedGdd": "gdd_rolling_total_cels",
        "accumulatedPpet": "ppet_rolling_total",
        "pet.amount": "pet_daily_total_mm",
        "accumulatedPrecipitation.amount": "precip_rolling_total_mm",
        "accumulatedPet.amount": "pet_rolling_total_mm"
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsFieldValues, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/agronomicvalues"

    def get_data(self, start_day=date.today().strftime("%m-%d"), end_day=None, offset=0):
        """Returns aWhere Forecast Agronomic Values for a provided field.
        """

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_values):
        """Extracts data from the aWhere agronomic forecast
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_values.get('location').get('latitude')
        longitude = agronomic_values.get('location').get('longitude')

        # Check if more than one day
        if agronomic_values.get('dailyValues'):

            # Do these with a separate call, just like in Soil accumulation='daily'
            #  accumulation='total'

            # DAILY ACCUMULATIONS
            # Get daily forecasted accumulations
            daily_accumulation = json_normalize(
                agronomic_values.get('dailyValues'))

            # Add lat/lon and set date as index
            daily_accumulation['latitude'] = latitude
            daily_accumulation['longitude'] = longitude
            daily_accumulation.set_index(['date'], inplace=True)

            # TOTAL ACCUMULATION
            # Get total forecasted accumulations through all days
            total_accumulation = json_normalize(
                agronomic_values.get('accumulations'))

            # Get list of dates, add start/end dates, set date range as index
            dates = [entry.get('date')
                     for entry in agronomic_values.get('dailyValues')]
            total_accumulation['date_range'] = f"{dates[0]}/{dates[-1]}"
            total_accumulation['start_day'] = dates[0]
            total_accumulation['end_day'] = dates[-1]
            total_accumulation.set_index(['date_range'], inplace=True)

            # Add lat/lon
            total_accumulation['latitude'] = latitude
            total_accumulation['longitude'] = longitude

            # Put dataframes in tuple (total accumulation, daily accumulation)
            agronomics_df = (total_accumulation, daily_accumulation)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_values)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(['date'], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type='single_day', kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if value_type.lower() == 'single_day':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map
            )

        elif value_type.lower() == 'multi_day':
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json)

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError("Invalid value type. Please choose 'single_day' or 'multi_day'.")

        return api_data_gdf


class AgronomicsFieldNorms(AgronomicsField):

    # Class variables for clean_data() function

    # https://developer.awhere.com/api/reference/agronomics/norms/geolocation

    """The average ratio of Precipitation to Potential Evapotranspiration
    over the years specified. When this value is above 1, then more rain fell
    than the amount of likely water loss; if it's below 1, then more water was
    likely lost than fell as rain. P/PET is most useful when calculated for a
    range of days, as it is for this property, than for individual days."""

    # Single day
    day_coord_cols = ['location.longitude', 'location.latitude']

    day_drop_cols = ['location.fieldId', 'pet.units', '_links.self.href',
                     '_links.curies', '_links.awhere:field.href']

    day_rename_map = {
        "gdd.average": "gdd_daily_average_total_cels",
        "gdd.stdDev": "gdd_daily_average_total_std_dev_cels",
        "pet.average": "pet_daily_average_total_mm",
        "pet.stdDev": "pet_daily_average_total_std_dev_mm",
        "ppet.average": "ppet_daily_average_total",
        "ppet.stdDev": "ppet_daily_average_total_std_dev"
    }

    # Multi-day, total accumulation
    total_coord_cols = ['longitude', 'latitude']

    total_drop_cols = ['precipitation.units', 'pet.units']

    total_rename_map = {
        "gdd.average": "gdd_range_average_total_cels",
        "gdd.stdDev": "gdd_range_average_total_std_dev_cels",
        "precipitation.average": "precip_range_average_total_mm",
        "precipitation.stdDev": "precip_range_average_total_std_dev_mm",
        "pet.average": "pet_range_average_total_mm",
        "pet.stdDev": "pet_range_average_total_std_dev",
        # Why doesn't this match with precip_avg/pet_avg?
        # What causes this difference?
        # Is it the average of each of individual PPET daily values?
        # Seems like it
        "ppet.average": "ppet_range_daily_average",
        "ppet.stdDev": "ppet_range_daily_average_std_dev"
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ['longitude', 'latitude']

    daily_drop_cols = ['pet.units', 'accumulatedPrecipitation.units',
                       'accumulatedPet.units', '_links.self.href',
                       '_links.curies', '_links.awhere:field.href']

    daily_rename_map = {
        "gdd.average": "gdd_daily_average_cels",
        "gdd.stdDev": "gdd_daily_average_std_dev_cels",
        "pet.average": "pet_daily_average_mm",
        "pet.stdDev": "pet_daily_average_std_dev_mm",
        "ppet.average": "ppet_daliy_average",
        "ppet.stdDev": "ppet_daily_average_std_dev",
        "accumulatedGdd.average": "gdd_rolling_total_average",
        "accumulatedGdd.stdDev": "gdd_rolling_total_average_std_dev",
        "accumulatedPrecipitation.average": "precip_rolling_total_average_mm",
        "accumulatedPrecipitation.stdDev": "precip_rolling_total_average_std_dev_mm",
        "accumulatedPet.average": "pet_rolling_total_average_mm",
        "accumulatedPet.stdDev": "pet_rolling_total_average_std_dev_mm",
        "accumulatedPpet.average": "ppet_rolling_total_average",
        "accumulatedPpet.stdDev": "ppet_rolling_total_average_std_dev"
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsFieldNorms, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/agronomicnorms"

    def get_data(self, start_day='01-01', end_day=None, offset=0):
        """Returns aWhere Historic Agronomic Norms.
        """

        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"

        # Get single day norms or date range
        response = requests.get(url_multiple_days, headers=auth_headers) if end_day else requests.get(
            url_single_day, headers=auth_headers)

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_norms):
        """Extracts data from the aWhere agronomic norms
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_norms.get('location').get('latitude')
        longitude = agronomic_norms.get('location').get('longitude')

        # Check if more than one day
        if agronomic_norms.get('dailyNorms'):

            # DAILY ACCUMULATION NORMS
            # Get daily accumulation norms
            daily_norms = json_normalize(
                agronomic_norms.get('dailyNorms'))

            # Add lat/lon and set date as index
            daily_norms['latitude'] = latitude
            daily_norms['longitude'] = longitude
            daily_norms.set_index(['day'], inplace=True)

            # TOTAL ACCUMULATION NORMS
            # Get average accumulations through all days
            total_norms = json_normalize(
                agronomic_norms.get('averageAccumulations'))

            # Get list of dates, add start/end dates, set date range as index
            dates = [entry.get('day')
                     for entry in agronomic_norms.get('dailyNorms')]
            total_norms['date_range'] = f"{dates[0]}/{dates[-1]}"
            total_norms['start_day'] = dates[0]
            total_norms['end_day'] = dates[-1]
            total_norms.set_index(['date_range'], inplace=True)

            # Add lat/lon
            total_norms['latitude'] = latitude
            total_norms['longitude'] = longitude

            # Put dataframes in tuple (total norms, daily norms)
            agronomics_df = (total_norms, daily_norms)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_norms)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(['day'], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type='single_day', kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = api_object.get_data(
            **kwargs) if kwargs else api_object.get_data()

        if value_type.lower() == 'single_day':
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map
            )

        elif value_type.lower() == 'multi_day':
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json)

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError("Invalid value type. Please choose 'single_day' or 'multi_day'.")

        return api_data_gdf


""" CROPS """


class AgronomicsCrops(Agronomics):

    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsCrops, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.api_url = f"{self.api_url}/crops"

    # field_id=None, crop_name=None, limit=10, offset=0
    def get(self, crop_id=None, limit=10, offset=0):
        """Retrieve a list of available crops.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Get API response, single crop or page of crops
        response = requests.get(f"{self.api_url}/{crop_id}", headers=auth_headers) if crop_id else requests.get(
            f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json) if crop_id else json_normalize(
            response_json.get('crops'))

        # Drop unnecessary columns
        response_df.drop(columns=[
            '_links.self.href', '_links.curies', '_links.awhere:plantings.href'
        ], inplace=True)

        # Reset index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column names
        crop_rename = {
            'id': 'crop_id',
            'name': 'crop_name',
            'type': 'crop_type',
            'variety': 'crop_variety',
            'isDefaultForCrop': 'default_crop'
        }

        # Rename columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df

    def get_full(self, limit=10, offset=0, max_pages=3):
        """Retrieves the full list of available crops,
        based on limit, offset, and max pages.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Define list to store page dataframes
        response_df_list = []

        # Loop through all pages
        while offset < limit * max_pages:

            # Get API response; convert response to dataframe; append to dataframe list
            response = requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)
            response_json = response.json()
            response_df_loop = json_normalize(response_json.get('crops'))
            response_df_list.append(response_df_loop)
            offset += 10

        # Merge all dataframes into a single dataframe
        response_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary dataframe columns
        response_df.drop(columns=[
            '_links.self.href', '_links.curies', '_links.awhere:plantings.href'
        ], inplace=True)

        # Reset dataframe index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column name mapping
        crop_rename = {
            'id': 'crop_id',
            'name': 'crop_name',
            'type': 'crop_type',
            'variety': 'crop_variety',
            'isDefaultForCrop': 'default_crop'
        }

        # Rename dataframe columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df


class AgronomicsCrop(AgronomicsCrops):

    def __init__(self, api_key, api_secret, crop_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsCrop, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.api_url = f"{self.api_url}/{crop_id}"

    def get(self):
        """Retrieves the information for the defined crop.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Get API response, single crop
        response = requests.get(f"{self.api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json)

        # Drop unnecessary columns
        response_df.drop(columns=[
            '_links.self.href', '_links.curies', '_links.awhere:plantings.href'
        ], inplace=True)

        # Reset index
        response_df.reset_index(drop=True, inplace=True)

        # Define new column names
        crop_rename = {
            'id': 'crop_id',
            'name': 'crop_name',
            'type': 'crop_type',
            'variety': 'crop_variety',
            'isDefaultForCrop': 'default_crop'
        }

        # Rename columns
        response_df.rename(columns=crop_rename, inplace=True)

        return response_df


""" PLANTINGS """


class AgronomicsFieldPlantings(AgronomicsField):

    # Define field_id intitializing class
    def __init__(self, api_key, api_secret, field_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsFieldPlantings, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

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
        response = requests.get(f"{self.api_url}/{planting_id}", headers=auth_headers) if planting_id else requests.get(
            f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json) if planting_id else json_normalize(
            response_json.get('plantings'))

        drop_cols = [
            '_links.self.href', '_links.curies',
            '_links.awhere:crop.href', '_links.awhere:field.href'
        ]

        # Drop unnecessary columns
        response_df.drop(
            columns=drop_cols, inplace=True)

        # Define new column names
        planting_rename = {
            'id': 'planting_id',
            'crop': 'crop_id',
            'field': 'field_id',
            'plantingDate': 'planting_date',
            'harvestDate': 'harvest_date_actual',
            # What is 'recommendation' field? What output goes here, and where does it come from?
            # {response_json.get("yield").get("units").lower()}',
            'yield.amount': 'yield_amount_actual',
            'yield.units': 'yield_amount_actual_units',
            # {response_json.get("projections").get("yield").get("units").lower()}',
            'projections.yield.amount': 'yield_amount_projected',
            'projections.yield.units': 'yield_amount_projected_units',
            'projections.harvestDate': 'harvest_date_projected'
        }

        # Rename
        response_df.rename(columns=planting_rename, inplace=True)

        # Set index
        response_df.set_index('planting_id', inplace=True)

        return response_df

    def create(self, crop, planting_date, projected_yield_amount=None, projected_yield_units=None,
               projected_harvest_date=None, yield_amount=None, yield_units=None, harvest_date=None):
        """Creates a planting in the field.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {str(self.auth_token)}",
            "Content-Type": 'application/json'
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
                "harvestDate": projected_harvest_date
            },
            "yield": {
                "amount": yield_amount,
                "units": yield_units,
            },
            "harvestDate": harvest_date
        }

        # Creat planting
        response = requests.post(
            self.api_url, headers=auth_headers, json=field_body)

        return response.json()

    def update(self, planting_id='current', update_type='replace', kwargs=None):
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
            "Content-Type": 'application/json'
        }

        # Full replace
        if update_type.lower() == 'replace':
            # Define request body
            field_body = {
                "crop": kwargs.get('crop'),
                "plantingDate": kwargs.get('planting_date'),
                "projections": {
                    "yield": {
                        "amount": kwargs.get('projected_yield_amount'),
                        "units": kwargs.get('projected_yield_units'),
                    },
                    "harvestDate": kwargs.get('projected_harvest_date')
                },
                "yield": {
                    "amount": kwargs.get('yield_amount'),
                    "units": kwargs.get('yield_units'),
                },
                "harvestDate": kwargs.get('harvest_date')
            }

            # Update planting
            response = requests.put(
                f"{self.api_url}/{planting_id}", headers=auth_headers, json=field_body)

        elif update_type.lower() == 'update':

            # Define field body
            field_body = [{"op": "replace", "path": f"/{key}", "value": f"{value}"}
                          for key, value in kwargs.items()]

            # Perform the HTTP request to update field information
            response = requests.patch(
                f"{self.api_url}/{planting_id}", headers=auth_headers, json=field_body)

        else:
            raise ValueError("Invalid update type. Please choose 'replace' or 'update'.")

        return response.json()

    def delete(self, planting_id='current'):
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
            f"{self.api_url}/{planting_id}", headers=auth_headers)

        message = f"Deleted planting: {planting_id}" if response.status_code == 204 else f"Could not delete planting."

        return print(message)


""" MODELS """


class AgronomicsModels(Agronomics):

    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsModels, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.api_url = f"{self.api_url}/models"

    def get(self, model_id=None, limit=10, offset=0):
        """Retrieve a list of available models.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Get API response, single crop or page of crops
        response = requests.get(f"{self.api_url}/{model_id}", headers=auth_headers) if model_id else requests.get(
            f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json) if model_id else json_normalize(
            response_json.get('models'))

        # Drop unnecessary columns
        response_df.drop(columns=[
            '_links.self.href', '_links.curies',
            '_links.awhere:crop', '_links.awhere:modelDetails.href'
        ], inplace=True)

        # Define new column names
        model_rename = {
            'id': 'model_id',
            'name': 'model_name',
            'description': 'model_description',
            'type': 'model_type',
            'source.name': 'model_source',
            'source.link': 'model_link'
        }

        # Rename columns
        response_df.rename(columns=model_rename, inplace=True)

        # Set index
        response_df.set_index('model_id', inplace=True)

        return response_df

    def get_full(self, limit=10, offset=0, max_pages=3):
        """Retrieves the full list of available models,
        based on limit, offset, and max pages.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Define list to store page dataframes
        response_df_list = []

        # Loop through all pages
        while offset < limit * max_pages:

            # Get API response; convert response to dataframe; append to dataframe list
            response = requests.get(
                f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)
            response_json = response.json()
            response_df_loop = json_normalize(response_json.get('models'))
            response_df_list.append(response_df_loop)
            offset += 10

        # Merge all dataframes into a single dataframe
        response_df = pd.concat(response_df_list, axis=0)

        # Drop unnecessary columns
        response_df.drop(columns=[
            '_links.self.href', '_links.curies',
            '_links.awhere:crop', '_links.awhere:modelDetails.href'
        ], inplace=True)

        # Define new column names
        model_rename = {
            'id': 'model_id',
            'name': 'model_name',
            'description': 'model_description',
            'type': 'model_type',
            'source.name': 'model_source',
            'source.link': 'model_link'
        }

        # Rename columns
        response_df.rename(columns=model_rename, inplace=True)

        # Set index
        response_df.set_index('model_id', inplace=True)

        return response_df

    def get_details(self, model_id='BarleyGenericMSU'):
        """Retrieve model details
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
        }

        # Get API response, single crop or page of crops
        response = requests.get(f"{self.api_url}/{model_id}/details", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Model base information
        base_info_df = json_normalize(response_json)
        base_info_df.drop(
            columns=[
                'gddUnits', 'stages', '_links.self.href',
                '_links.curies', '_links.awhere:model.href'
            ], inplace=True)
        base_info_df['model_id'] = model_id
        base_info_df.set_index('model_id', inplace=True)
        base_info_df.rename(columns={
            'biofix': 'biofix_days',
            'gddMethod': 'gdd_method',
            'gddBaseTemp': 'gdd_base_temp_cels',
            'gddMaxBoundary': 'gdd_max_boundary_cels',
            'gddMinBoundary': 'gdd_min_boundary_cels'
        }, inplace=True)

        # Model stage information
        stage_info_df = json_normalize(response_json.get('stages'))
        stage_info_df.drop(columns=['gddUnits'], inplace=True)
        stage_info_df['model_id'] = model_id
        stage_info_df.rename(columns={
            'id': 'stage_id',
            'stage': 'stage_name',
            'description': 'stage_description',
            'gddThreshold': 'gdd_threshold_cels',
        }, inplace=True)
        stage_info_df.set_index(['model_id', 'stage_id'], inplace=True)

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


""" PLANTINGS """


class AgronomicsPlantings(Agronomics):

    def __init__(self, api_key, api_secret, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsPlantings, self).__init__(api_key, api_secret,
                                                  base_64_encoded_secret_key, auth_token)

        self.api_url = f'{self.api_url}/plantings'

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
        response = requests.get(f"{self.api_url}/{planting_id}", headers=auth_headers) if planting_id else requests.get(
            f"{self.api_url}?limit={limit}&offset={offset}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Convert to dataframe
        response_df = json_normalize(response_json.get('plantings')) if response_json.get(
            'plantings') else json_normalize(response_json)

        drop_cols = [
            '_links.self.href', '_links.curies',
            '_links.awhere:crop.href', '_links.awhere:field.href'
        ]

        # Drop unnecessary columns
        response_df.drop(
            columns=drop_cols, inplace=True)

        # Define new column names
        planting_rename = {
            'id': 'planting_id',
            'crop': 'crop_id',
            'field': 'field_id',
            'plantingDate': 'planting_date',
            'harvestDate': 'harvest_date_actual',
            # What is 'recommendation' field? What output goes here, and where does it come from?
            # {response_json.get("yield").get("units").lower()}',
            'yield.amount': 'yield_amount_actual',
            'yield.units': 'yield_amount_actual_units',
            # {response_json.get("projections").get("yield").get("units").lower()}',
            'projections.yield.amount': 'yield_amount_projected',
            'projections.yield.units': 'yield_amount_projected_units',
            'projections.harvestDate': 'harvest_date_projected'
        }

        # Rename
        response_df.rename(columns=planting_rename, inplace=True)

        # Set index
        response_df.set_index('planting_id', inplace=True)

        return response_df

    def get_full(self):
        """Retrieves the full list of plantings associated
        with an aWhere account.
        """
        pass


""" MODELS """


class AgronomicsFieldModels(AgronomicsField):

    # Define field_id intitializing class
    def __init__(self, api_key, api_secret, field_id, model_id, base_64_encoded_secret_key=None,
                 auth_token=None, api_url=None):

        super(AgronomicsFieldModels, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token, api_url)

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/models/{model_id}/results"

    def get(self):
        """Returns aWhere model associated with a field.
        """
        # Setup the HTTP request headers
        auth_headers = {
            "Authorization": f"Bearer {self.auth_token}"
            # "Content-Type": 'application/json'
        }

        # Get API response
        response = requests.get(
            f"{self.api_url}", headers=auth_headers)

        # Convert API response to JSON format
        response_json = response.json()

        # Get stage info
        previous_stage_df = json_normalize(response_json.get('previousStages'))
        current_stage_df = json_normalize(response_json.get('currentStage'))
        next_stage_df = json_normalize(response_json.get('nextStage'))

        # Add columns
        previous_stage_df['stage_status'] = 'Previous'
        current_stage_df['stage_status'] = 'Current'
        next_stage_df['stage_status'] = 'Next'

        # Merge into one dataframe
        stages_df = pd.concat([
            previous_stage_df, current_stage_df, next_stage_df],
            sort=False, axis=0)

        # Change column names
        stages_df.rename(columns={
            'date': 'stage_start_date',
            'id': 'stage_id',
            'stage': 'stage_name',
            'description': 'stage_description',
            'gddThreshold': 'gdd_threshold_cels',
            'accumulatedGdds': 'gdd_accumulation_current_cels',
            'gddRemaining': 'gdd_remaining_next_cels'
        }, inplace=True)

        # Add base data
        stages_df['biofix_date'] = response_json.get('biofixDate')
        stages_df['planting_date'] = response_json.get('plantingDate')
        stages_df['model_id'] = response_json.get('modelId')
        stages_df['field_id'] = response_json.get('location').get('fieldId')
        stages_df['longitude'] = response_json.get('location').get('longitude')
        stages_df['latitude'] = response_json.get('location').get('latitude')

        # Set index
        stages_df.set_index(['field_id', 'stage_status'], inplace=True)

        # Prep for geodataframe conversion
        df_copy = stages_df.copy()

        # Define CRS (EPSG 4326)
        crs = {'init': 'epsg:4326'}

        # Convert to geodataframe
        stages_gdf = gpd.GeoDataFrame(
            df_copy, crs=crs, geometry=gpd.points_from_xy(
                stages_df.longitude,
                stages_df.latitude)
        )

        # Drop lat/lon
        stages_gdf.drop(columns=['longitude', 'latitude'], inplace=True)

        # Reorder columns
        stages_gdf = stages_gdf.reindex(columns=[
            'model_id', 'biofix_date', 'planting_date',
            'stage_start_date', 'stage_id', 'stage_name',
            'stage_description', 'gdd_threshold_cels',
            'gdd_accumulation_current_cels', 'gdd_remaining_next_cels',
            'geometry'
        ])

        return stages_gdf


if __name__ == '__main__':
    # Imports
    import os

    # Show all pandas columns
    pd.set_option('max_columns', None)

    # Define aWhere API key and secret
    api_key = os.environ.get('AWHERE_API_KEY')
    api_secret = os.environ.get('AWHERE_API_SECRET')

    # Define aWhere weather objects, Bear Lake, RMNP, Colorado
    norms_object = WeatherLocationNorms(
        api_key, api_secret, latitude=40.313250, longitude=-105.648222)
    observed_object = WeatherLocationObserved(
        api_key, api_secret, latitude=40.313250, longitude=-105.648222)
    forecast_object = WeatherLocationForecast(
        api_key, api_secret, latitude=40.313250, longitude=-105.648222)

    # Create geodataframes
    norms_gdf = WeatherLocationNorms.api_to_gdf(norms_object)
    observed_gdf = WeatherLocationObserved.api_to_gdf(observed_object)
    forecast_main_gdf = WeatherLocationForecast.api_to_gdf(forecast_object, forecast_type='main')
    forecast_soil_gdf = WeatherLocationForecast.api_to_gdf(forecast_object, forecast_type='soil')

    # Display geodataframes
    print(norms_gdf.head())
    print(observed_gdf.head())
    print(forecast_main_gdf.head())
    print(forecast_soil_gdf.head())
