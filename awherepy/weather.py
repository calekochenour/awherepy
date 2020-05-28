"""
awherepy.weather
================
A module to access and retrieve aWhere weather data.
"""

import requests
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
from awherepy import AWhereAPI


class Weather(AWhereAPI):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):
        super(Weather, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = "https://api.awhere.com/v2/weather"

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
        crs = "epsg:4326"

        # Rename index - possibly as option, or take care of index prior?
        # df.index.rename('date_rename', inplace=True)

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                df[lon_lat_cols[0]], df[lon_lat_cols[1]]
            ),
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
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        api_data_df = cls.extract_data(api_data_json)

        api_data_gdf = cls.clean_data(
            api_data_df, cls.coord_cols, cls.drop_cols, cls.rename_map
        )

        return api_data_gdf


class WeatherLocation(Weather):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherLocation, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.api_url = f"{self.api_url}/locations"


class WeatherField(Weather):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherField, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.api_url = f"{self.api_url}/fields"


class WeatherLocationNorms(WeatherLocation):
    # Class variables for clean_data() function
    coord_cols = ["location.longitude", "location.latitude"]

    drop_cols = [
        "meanTemp.units",
        "maxTemp.units",
        "minTemp.units",
        "precipitation.units",
        "solar.units",
        "dailyMaxWind.units",
        "averageWind.units",
    ]

    rename_map = {
        "meanTemp.average": "mean_temp_avg_cels",
        "meanTemp.stdDev": "mean_temp_std_dev_cels",
        "maxTemp.average": "max_temp_avg_cels",
        "maxTemp.stdDev": "max_temp_std_dev_cels",
        "minTemp.average": "min_temp_avg_cels",
        "minTemp.stdDev": "min_temp_std_dev_cels",
        "precipitation.average": "precip_avg_mm",
        "precipitation.stdDev": "precip_std_dev_mm",
        "solar.average": "solar_avg_w_h_per_m2",
        "solar.stdDev": "solar_avg_std_dev_w_h_per_m2",
        "minHumidity.average": "min_humiduty_avg_%",
        "minHumidity.stdDev": "min_humidity_std_dev_%",
        "maxHumidity.average": "max_humiduty_avg_%",
        "maxHumidity.stdDev": "max_humidity_std_dev_%",
        "dailyMaxWind.average": "daily_max_wind_avg_m_per_sec",
        "dailyMaxWind.stdDev": "daily_max_wind_std_dev_m_per_sec",
        "averageWind.average": "average_wind_m_per_sec",
        "averageWind.stdDev": "average_wind_std_dev_m_per_sec",
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        latitude,
        longitude,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherLocationNorms, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = f"{self.api_url}/{self.latitude},{self.longitude}/norms"

    def get_data(self, start_day="01-01", end_day=None, offset=0):
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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}?limit=10&offset={offset}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

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
        if historic_norms.get("norms"):
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms.get("norms"))

        # Single-day norm
        else:
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms)

        # Set day as index
        historic_norms_df.set_index("day", inplace=True)

        # Drop unnecessary columns
        historic_norms_df.drop(
            columns=["_links.self.href"], axis=1, inplace=True
        )

        # Return dataframe
        return historic_norms_df


class WeatherLocationObserved(WeatherLocation):
    # Class variables for clean_data() function
    coord_cols = ["location.longitude", "location.latitude"]

    drop_cols = [
        "temperatures.units",
        "precipitation.units",
        "solar.units",
        "wind.units",
    ]

    rename_map = {
        "temperatures.max": "temp_max_cels",
        "temperatures.min": "temp_min_cels",
        "precipitation.amount": "precip_amount_mm",
        "solar.amount": "solar_energy_w_h_per_m2",
        "relativeHumidity.average": "rel_humidity_avg_%",
        "relativeHumidity.max": "rel_humidity_max_%",
        "relativeHumidity.min": "rel_humidity_min_%",
        "wind.morningMax": "wind_morning_max_m_per_sec",
        "wind.dayMax": "wind_day_max_m_per_sec",
        "wind.average": "wind_avg_m_per_sec",
    }

    def __init__(
        self,
        api_key,
        api_secret,
        latitude,
        longitude,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherLocationObserved, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = (
            f"{self.api_url}/{self.latitude},{self.longitude}/observations"
        )

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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Define URL variants
        url_no_date = f"{self.api_url}?limit=10&offset={offset}"
        url_start_date = f"{self.api_url}/{start_day}"
        url_end_date = f"{self.api_url}/{end_day}"
        url_both_dates = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

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
        if observed_weather.get("observations"):
            # Flatten to dataframe
            observed_weather_df = json_normalize(
                observed_weather.get("observations")
            )

        # Single-day observed
        else:
            # Flatten to dataframe
            observed_weather_df = json_normalize(observed_weather)

        # Set date as index
        observed_weather_df.set_index("date", inplace=True)

        # Drop unnecessary columns
        observed_weather_df.drop(
            columns=["_links.self.href"], axis=1, inplace=True
        )

        # Return dataframe
        return observed_weather_df


class WeatherLocationForecast(WeatherLocation):
    # Class variables for clean_data() function
    # Main forecast
    coord_cols = ["longitude", "latitude"]

    drop_cols = [
        "temperatures.units",
        "precipitation.units",
        "solar.units",
        "wind.units",
        "dewPoint.units",
    ]

    rename_map = {
        "startTime": "start_time",
        "endTime": "end_time",
        "conditionsCode": "conditions_code",
        "conditionsText": "conditions_text",
        "temperatures.max": "temp_max_cels",
        "temperatures.min": "temp_min_cels",
        "precipitation.chance": "precip_chance_%",
        "precipitation.amount": "precip_amount_mm",
        "sky.cloudCover": "sky_cloud_cover_%",
        "sky.sunshine": "sky_sunshine_%",
        "solar.amount": "solar_energy_w_h_per_m2",
        "relativeHumidity.average": "rel_humidity_avg_%",
        "relativeHumidity.max": "rel_humidity_max_%",
        "relativeHumidity.min": "rel_humidity_min_%",
        "wind.average": "wind_avg_m_per_sec",
        "wind.max": "wind_max_m_per_sec",
        "wind.min": "wind_min_m_per_sec",
        "wind.bearing": "wind_bearing_deg",
        "wind.direction": "wind_direction_compass",
        "dewPoint.amount": "dew_point_cels",
    }

    # Soil
    soil_coord_cols = ["longitude", "latitude"]

    soil_drop_cols = ["units"]

    soil_rename_map = {
        "average_temp": "soil_temp_avg_cels",
        "max_temp": "soil_temp_max_cels",
        "min_temp": "soil_temp_min_cels",
        "average_moisture": "soil_moisture_avg_%",
        "max_moisture": "soil_moisture_max_%",
        "min_moisture": "soil_moisture_min_%",
    }

    def __init__(
        self,
        api_key,
        api_secret,
        latitude,
        longitude,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherLocationForecast, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = (
            f"{self.api_url}/{self.latitude},{self.longitude}/forecasts"
        )

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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Define URL variants
        url_no_date = (
            f"{self.api_url}?limit=10&offset={offset}&blockSize={block_size}"
        )
        url_start_date = f"{self.api_url}/{start_day}?limit=10&offset="
        f"{offset}&blockSize={block_size}"
        url_end_date = f"{self.api_url}/{end_day}?limit=10&offset="
        f"{offset}&blockSize={block_size}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&"
        f"offset={offset}&blockSize={block_size}"

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
        if forecast.get("forecasts"):
            forecast_iterator = json_normalize(forecast.get("forecasts"))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level
            #  dataframe outputs
            date = row["date"]
            lat = row["location.latitude"]
            lon = row["location.longitude"]

            # Extract the main forecast from the top-level dataframe
            forecast = row["forecast"]

            # Faltten data into dataframe
            forecast_norm = json_normalize(forecast)

            # Drop soil moisture and soil temperature columns
            #  (will be extracted as indivdiual dataframes)
            forecast_norm.drop(
                columns=["soilTemperatures", "soilMoisture"],
                axis=1,
                inplace=True,
            )
            # Assign date, lat/lon to dataframe
            forecast_norm["date"] = date
            forecast_norm["latitude"] = lat
            forecast_norm["longitude"] = lon

            # Set date as index
            forecast_norm.set_index(["date"], inplace=True)

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
        if forecast.get("forecasts"):
            forecast_iterator = json_normalize(forecast.get("forecasts"))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level
            #  dataframe outputs
            date = row["date"]
            lat = row["location.latitude"]
            lon = row["location.longitude"]

            # Get soil temperature data
            forecast_soil_temp = row["forecast"][0].get("soilTemperatures")
            forecast_soil_moisture = row["forecast"][0].get("soilMoisture")

            # Flatten data into dataframe
            forecast_soil_temp_df = json_normalize(forecast_soil_temp)
            forecast_soil_moisture_df = json_normalize(forecast_soil_moisture)

            # Combine temperature and moisture
            forecast_soil_df = forecast_soil_temp_df.merge(
                forecast_soil_moisture_df,
                on="depth",
                suffixes=("_temp", "_moisture"),
            )

            # Assign date, lat/lon to dataframe
            forecast_soil_df["date"] = date
            forecast_soil_df["latitude"] = lat
            forecast_soil_df["longitude"] = lon

            # Shorten depth values to numerics (will be used in MultiIndex)
            forecast_soil_df["depth"] = forecast_soil_df["depth"].apply(
                lambda x: x[0:-15]
            )

            # Rename depth prior to indexing
            forecast_soil_df.rename(
                columns={"depth": "ground_depth_m"}, inplace=True
            )

            # Create multi-index dataframe for date and soil
            #  depth (rename depth columns? rather long)
            soil_multi_index = forecast_soil_df.set_index(
                ["date", "ground_depth_m"]
            )

            # Add dataframe to list of dataframes
            forecast_soil_list.append(soil_multi_index)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_soil_list)

    @classmethod
    def api_to_gdf(cls, api_object, forecast_type="main", kwargs=None):
        """
        forecast_type can either be 'main' or 'soil'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if forecast_type.lower() == "main":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df, cls.coord_cols, cls.drop_cols, cls.rename_map
            )

        elif forecast_type.lower() == "soil":
            api_data_df = cls.extract_soil(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.soil_coord_cols,
                cls.soil_drop_cols,
                cls.soil_rename_map,
            )

        else:
            raise ValueError(
                "Invalid forecast type. Please choose 'main' or 'soil'."
            )

        return api_data_gdf


class WeatherFieldNorms(WeatherField):
    # Class variables for clean_data() function
    coord_cols = ["location.longitude", "location.latitude"]

    drop_cols = [
        "location.fieldId",
        "meanTemp.units",
        "maxTemp.units",
        "minTemp.units",
        "precipitation.units",
        "solar.units",
        "dailyMaxWind.units",
        "averageWind.units",
    ]

    rename_map = {
        "meanTemp.average": "mean_temp_avg_cels",
        "meanTemp.stdDev": "mean_temp_std_dev_cels",
        "maxTemp.average": "max_temp_avg_cels",
        "maxTemp.stdDev": "max_temp_std_dev_cels",
        "minTemp.average": "min_temp_avg_cels",
        "minTemp.stdDev": "min_temp_std_dev_cels",
        "precipitation.average": "precip_avg_mm",
        "precipitation.stdDev": "precip_std_dev_mm",
        "solar.average": "solar_avg_w_h_per_m2",
        "minHumidity.average": "min_humiduty_avg_%",
        "minHumidity.stdDev": "min_humidity_std_dev_%",
        "maxHumidity.average": "max_humiduty_avg_%",
        "maxHumidity.stdDev": "max_humidity_std_dev_%",
        "dailyMaxWind.average": "daily_max_wind_avg_m_per_sec",
        "dailyMaxWind.stdDev": "daily_max_wind_std_dev_m_per_sec",
        "averageWind.average": "average_wind_m_per_sec",
        "averageWind.stdDev": "average_wind_std_dev_m_per_sec",
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherFieldNorms, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/norms"

    def get_data(self, start_day="01-01", end_day=None, offset=0):
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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}?limit=10&offset={offset}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

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
        if historic_norms.get("norms"):
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms.get("norms"))

        # Single-day norm
        else:
            # Flatten to dataframe
            historic_norms_df = json_normalize(historic_norms)

        # Set day as index
        historic_norms_df.set_index("day", inplace=True)

        # Drop unnecessary columns
        historic_norms_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:field.href",
            ],
            axis=1,
            inplace=True,
        )

        # Return dataframe
        return historic_norms_df


class WeatherFieldObserved(WeatherField):
    # Class variables for clean_data() function
    coord_cols = ["location.longitude", "location.latitude"]

    drop_cols = [
        "location.fieldId",
        "temperatures.units",
        "precipitation.units",
        "solar.units",
        "wind.units",
    ]

    rename_map = {
        "temperatures.max": "temp_max_cels",
        "temperatures.min": "temp_min_cels",
        "precipitation.amount": "precip_amount_mm",
        "solar.amount": "solar_energy_w_h_per_m2",
        "relativeHumidity.average": "rel_humidity_avg_%",
        "relativeHumidity.max": "rel_humidity_max_%",
        "relativeHumidity.min": "rel_humidity_min_%",
        "wind.morningMax": "wind_morning_max_m_per_sec",
        "wind.dayMax": "wind_day_max_m_per_sec",
        "wind.average": "wind_avg_m_per_sec",
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherFieldObserved, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Define URL variants
        url_no_date = f"{self.api_url}?limit=10&offset={offset}"
        url_start_date = f"{self.api_url}/{start_day}"
        url_end_date = f"{self.api_url}/{end_day}"
        url_both_dates = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

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
        if observed_weather.get("observations"):
            # Flatten to dataframe
            observed_weather_df = json_normalize(
                observed_weather.get("observations")
            )

        # Single-day observed
        else:
            # Flatten to dataframe
            observed_weather_df = json_normalize(observed_weather)

        # Set date as index
        observed_weather_df.set_index("date", inplace=True)

        # Drop unnecessary columns
        observed_weather_df.drop(
            columns=[
                "_links.self.href",
                "_links.curies",
                "_links.awhere:field.href",
            ],
            axis=1,
            inplace=True,
        )

        # Return dataframe
        return observed_weather_df


class WeatherFieldForecast(WeatherField):
    # Class variables for clean_data() function
    # Main forecast
    coord_cols = ["longitude", "latitude"]

    drop_cols = [
        "temperatures.units",
        "precipitation.units",
        "solar.units",
        "wind.units",
        "dewPoint.units",
    ]

    rename_map = {
        "startTime": "start_time",
        "endTime": "end_time",
        "conditionsCode": "conditions_code",
        "conditionsText": "conditions_text",
        "temperatures.max": "temp_max_cels",
        "temperatures.min": "temp_min_cels",
        "precipitation.chance": "precip_chance_%",
        "precipitation.amount": "precip_amount_mm",
        "sky.cloudCover": "sky_cloud_cover_%",
        "sky.sunshine": "sky_sunshine_%",
        "solar.amount": "solar_energy_w_h_per_m2",
        "relativeHumidity.average": "rel_humidity_avg_%",
        "relativeHumidity.max": "rel_humidity_max_%",
        "relativeHumidity.min": "rel_humidity_min_%",
        "wind.average": "wind_avg_m_per_sec",
        "wind.max": "wind_max_m_per_sec",
        "wind.min": "wind_min_m_per_sec",
        "wind.bearing": "wind_bearing_deg",
        "wind.direction": "wind_direction_compass",
        "dewPoint.amount": "dew_point_cels",
    }

    # Soil
    soil_coord_cols = ["longitude", "latitude"]

    soil_drop_cols = ["units"]

    soil_rename_map = {
        "average_temp": "soil_temp_avg_cels",
        "max_temp": "soil_temp_max_cels",
        "min_temp": "soil_temp_min_cels",
        "average_moisture": "soil_moisture_avg_%",
        "max_moisture": "soil_moisture_max_%",
        "min_moisture": "soil_moisture_min_%",
    }

    # Define field when intitializing class; no need to repeat for field
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(WeatherFieldForecast, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

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
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Define URL variants
        url_no_date = (
            f"{self.api_url}?limit=10&offset={offset}&blockSize={block_size}"
        )
        url_start_date = f"{self.api_url}/{start_day}?limit=10&offset={offset}"
        f"&blockSize={block_size}"
        url_end_date = f"{self.api_url}/{end_day}?limit=10&offset={offset}"
        f"&blockSize={block_size}"
        url_both_dates = f"{self.api_url}/{start_day},{end_day}?limit=10&"
        f"offset={offset}&blockSize={block_size}"

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
        if forecast.get("forecasts"):
            forecast_iterator = json_normalize(forecast.get("forecasts"))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level
            #  dataframe outputs
            date = row["date"]
            lat = row["location.latitude"]
            lon = row["location.longitude"]

            # Extract the main forecast from the top-level dataframe
            forecast = row["forecast"]

            # Faltten data into dataframe
            forecast_norm = json_normalize(forecast)

            # Drop soil moisture and soil temperature columns
            #  (will be extracted as indivdiual dataframes)
            forecast_norm.drop(
                columns=["soilTemperatures", "soilMoisture"],
                axis=1,
                inplace=True,
            )

            # Assign date, lat/lon to dataframe
            forecast_norm["date"] = date
            forecast_norm["latitude"] = lat
            forecast_norm["longitude"] = lon

            # Set date as index
            forecast_norm.set_index(["date"], inplace=True)

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
        if forecast.get("forecasts"):
            forecast_iterator = json_normalize(forecast.get("forecasts"))

        # Single day
        else:
            forecast_iterator = json_normalize(forecast)

        # Loop through each row in the top-level flattened dataframe
        for index, row in forecast_iterator.iterrows():

            # Extract date, lat, lon for insertion into lower-level
            #  dataframe outputs
            date = row["date"]
            lat = row["location.latitude"]
            lon = row["location.longitude"]

            # Get soil temperature data
            forecast_soil_temp = row["forecast"][0].get("soilTemperatures")
            forecast_soil_moisture = row["forecast"][0].get("soilMoisture")

            # Flatten data into dataframe
            forecast_soil_temp_df = json_normalize(forecast_soil_temp)
            forecast_soil_moisture_df = json_normalize(forecast_soil_moisture)

            # Combine temperature and moisture
            forecast_soil_df = forecast_soil_temp_df.merge(
                forecast_soil_moisture_df,
                on="depth",
                suffixes=("_temp", "_moisture"),
            )

            # Assign date, lat/lon to dataframe
            forecast_soil_df["date"] = date
            forecast_soil_df["latitude"] = lat
            forecast_soil_df["longitude"] = lon

            # Shorten depth values to numerics (will be used in MultiIndex)
            forecast_soil_df["depth"] = forecast_soil_df["depth"].apply(
                lambda x: x[0:-15]
            )

            # Rename depth prior to indexing
            forecast_soil_df.rename(
                columns={"depth": "ground_depth_m"}, inplace=True
            )

            # Create multi-index dataframe for date and soil depth
            #  (rename depth columns? rather long)
            soil_multi_index = forecast_soil_df.set_index(
                ["date", "ground_depth_m"]
            )

            # Add dataframe to list of dataframes
            forecast_soil_list.append(soil_multi_index)

        # Return merged lists of dataframes into a single dataframe
        return pd.concat(forecast_soil_list)

    @classmethod
    def api_to_gdf(cls, api_object, forecast_type="main", kwargs=None):
        """
        forecast_type can either be 'main' or 'soil'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if forecast_type.lower() == "main":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df, cls.coord_cols, cls.drop_cols, cls.rename_map
            )

        elif forecast_type.lower() == "soil":
            api_data_df = cls.extract_soil(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.soil_coord_cols,
                cls.soil_drop_cols,
                cls.soil_rename_map,
            )

        else:
            raise ValueError(
                "Invalid forecast type. Please choose 'main' or 'soil'."
            )

        return api_data_gdf
