"""
awherepy.weather
================
A module to access and retrieve aWhere weather data.
"""

import requests as rq
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
import awherepy as aw

# Define variables for data cleaning
# Weather norms
NORMS_COORD_COLS = ["location.longitude", "location.latitude"]

NORMS_DROP_COLS = [
    "meanTemp.units",
    "maxTemp.units",
    "minTemp.units",
    "precipitation.units",
    "solar.units",
    "dailyMaxWind.units",
    "averageWind.units",
    "_links.curies",
    "_links.awhere:field.href",
]

NORMS_RENAME_MAP = {
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
    "location.fieldId": "field_id",
}

# Observed weather
OBSERVED_COORD_COLS = ["location.longitude", "location.latitude"]

OBSERVED_DROP_COLS = [
    "temperatures.units",
    "precipitation.units",
    "solar.units",
    "wind.units",
    "_links.curies",
    "_links.awhere:field.href",
]

OBSERVED_RENAME_MAP = {
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
    "location.fieldId": "field_id",
}

# Weather forecast
FORECAST_COORD_COLS = ["longitude", "latitude"]

FORECAST_DROP_COLS = [
    "temperatures.units",
    "precipitation.units",
    "solar.units",
    "wind.units",
    "dewPoint.units",
    "units",
]

FORECAST_RENAME_MAP = {
    "startTime": "start_time",
    "endTime": "end_time",
    "conditionsCode": "conditions_code",
    "conditionsText": "conditions_text",
    "temperatures.value": "temp_val_cels",
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
    "average_temp": "soil_temp_avg_cels",
    "max_temp": "soil_temp_max_cels",
    "min_temp": "soil_temp_min_cels",
    "average_moisture": "soil_moisture_avg_%",
    "max_moisture": "soil_moisture_max_%",
    "min_moisture": "soil_moisture_min_%",
}


def _call_weather_norms(
    key,
    secret,
    input_type="location",
    location=(-105.648222, 40.313250),
    field_id=None,
    start_date="01-01",
    end_date=None,
    limit=10,
    offset=0,
):
    """Retrieves weather data from the aWhere API,
    based on input parameters.
    """
    # Check input data type
    # Location-based
    if input_type == "location":

        # Raise error if location is not defined
        if location is None:
            raise ValueError("Must specify a location (longitude, latitude).")

        # Set URL to location
        api_url = (
            "https://api.awhere.com/v2/weather/locations/"
            f"{location[1]},{location[0]}"
        )

    # Field-based
    elif input_type == "field":

        # Raise error if field name is not defined
        if field_id is None:
            raise ValueError("Must specify a field name ('test-field').")

        # Set URL to fields
        api_url = f"https://api.awhere.com/v2/weather/fields/{field_id}"

    # Invalid input
    else:
        raise ValueError("Invalid date type. Must be 'location' or 'field'.")

    # Get OAuth token
    auth_token = aw.get_oauth_token(key, secret)

    # Set up the HTTP request headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Define URL variants - location
    url_single_day = (
        f"{api_url}/norms/{start_date}?limit={limit}&offset={offset}"
    )
    url_multiple_days = (
        f"{api_url}/norms/{start_date},{end_date}"
        f"?limit={limit}&offset={offset}"
    )

    # Get single-day or multi-day norms
    response = (
        rq.get(url_multiple_days, headers=auth_headers)
        if end_date
        else rq.get(url_single_day, headers=auth_headers)
    )

    # Convert response to json format
    weather_norms = response.json()

    # Return norms
    return weather_norms


def _extract_weather_norms(historic_norms):
    """Extracts weather data from the aWhere API
    return.

    Creates a dataframe from a JSON-like
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
    # Raise error if input is not of type dictionary
    if not isinstance(historic_norms, dict):
        raise TypeError("Input data must be a dictionary.")

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
    historic_norms_df.drop(columns=["_links.self.href"], axis=1, inplace=True)

    # Return dataframe
    return historic_norms_df


def _clean_weather_norms(df):
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
    # Define global variables
    global NORMS_COORD_COLS, NORMS_DROP_COLS, NORMS_RENAME_MAP

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    # Create copy of input dataframe; prevents altering the original
    df_copy = df.copy()

    # Convert to geodataframe
    gdf = gpd.GeoDataFrame(
        df_copy,
        crs=crs,
        geometry=gpd.points_from_xy(
            df[NORMS_COORD_COLS[0]], df[NORMS_COORD_COLS[1]]
        ),
    )

    # Add lat/lon columns to drop columns list
    NORMS_DROP_COLS += NORMS_COORD_COLS

    # Drop columns
    gdf.drop(columns=NORMS_DROP_COLS, axis=1, inplace=True, errors="ignore")

    # Rename columns
    gdf.rename(columns=NORMS_RENAME_MAP, inplace=True, errors="ignore")

    # Return cleaned up geodataframe
    return gdf


def get_weather_norms(key, secret, kwargs=None):
    """kwargs is a dictionary that provides values beyond the default;
    unpack dictionary if it exists

    kwargs are the parameters to get_data() method

    kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}

    input_type='location' 'field'

    kwargs : dict
        input_type="location",
        location=(-105.648222, 40.313250),
        field_id=None,
        start_date="01-01",
        end_date=None,
        limit=10,
        offset=0,

    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get data
        norms_json = (
            _call_weather_norms(key, secret, **kwargs)
            if kwargs
            else _call_weather_norms(key, secret)
        )

        # Extract data
        norms_df = _extract_weather_norms(norms_json)

        # Clean data
        norms_gdf = _clean_weather_norms(norms_df)

    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return cleaned data
    return norms_gdf


def _call_weather_observed(
    key,
    secret,
    input_type="location",
    location=(-105.648222, 40.313250),
    field_id=None,
    start_date=None,
    end_date=None,
    limit=10,
    offset=0,
):
    """Retrieves observed weather data from the
    aWhere API, based on input parameters.

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
    # Check input data type
    # Location-based
    if input_type == "location":

        # Raise error if location is not defined
        if location is None:
            raise ValueError("Must specify a location (longitude, latitude).")

        # Set URL to location
        api_url = (
            "https://api.awhere.com/v2/weather/locations/"
            f"{location[1]},{location[0]}"
        )

    # Field-based
    elif input_type == "field":

        # Raise error if field name is not defined
        if field_id is None:
            raise ValueError("Must specify a field name ('test-field').")

        # Set URL to fields
        api_url = f"https://api.awhere.com/v2/weather/fields/{field_id}"

    # Invalid input
    else:
        raise ValueError("Invalid date type. Must be 'location' or 'field'.")

    # Get OAuth token
    auth_token = aw.get_oauth_token(key, secret)

    # Set up the HTTP request headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Define URL variants
    url_no_date = f"{api_url}/observations?limit={limit}&offset={offset}"
    url_start_date = f"{api_url}/observations/{start_date}"
    url_end_date = f"{api_url}/observations/{end_date}"
    url_both_dates = (
        f"{api_url}/observations/{start_date},{end_date}"
        f"?limit={limit}&offset={offset}"
    )

    # Perform the HTTP request to obtain the norms for the Field
    # Default - 7-day
    if not (start_date or end_date):
        response = rq.get(url_no_date, headers=auth_headers)

    # Single date - specify start date
    elif start_date and not end_date:
        response = rq.get(url_start_date, headers=auth_headers)

    # Single date - specify end date
    elif end_date and not start_date:
        response = rq.get(url_end_date, headers=auth_headers)

    # Date range
    elif start_date and end_date:
        response = rq.get(url_both_dates, headers=auth_headers)

    # Convert response to json format
    weather_observed = response.json()

    # Return the observed
    return weather_observed


def _extract_weather_observed(observed_weather):
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
    # Raise error if input is not of type dictionary
    if not isinstance(observed_weather, dict):
        raise TypeError("Input data must be a dictionary.")

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


def _clean_weather_observed(df):
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
    # Define global variables
    global OBSERVED_COORD_COLS, OBSERVED_DROP_COLS, OBSERVED_RENAME_MAP

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    # Create copy of input dataframe; prevents altering the original
    df_copy = df.copy()

    # Convert to geodataframe
    gdf = gpd.GeoDataFrame(
        df_copy,
        crs=crs,
        geometry=gpd.points_from_xy(
            df[OBSERVED_COORD_COLS[0]], df[OBSERVED_COORD_COLS[1]]
        ),
    )

    # Add lat/lon columns to drop columns list
    OBSERVED_DROP_COLS += OBSERVED_COORD_COLS

    # Drop columns
    gdf.drop(columns=OBSERVED_DROP_COLS, axis=1, inplace=True, errors="ignore")

    # Rename columns
    gdf.rename(columns=OBSERVED_RENAME_MAP, inplace=True, errors="ignore")

    # Return cleaned up geodataframe
    return gdf


def get_weather_observed(key, secret, kwargs=None):
    """kwargs is a dictionary that provides values beyond the default;
    unpack dictionary if it exists

    kwargs are the parameters to get_data() method

    kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}

    input_type='location' 'field'

    kwargs : dict
        input_type="location",
        location=(-105.648222, 40.313250),
        field_id=None,
        start_date="01-01",
        end_date=None,
        limit=10,
        offset=0,
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        observed_json = (
            _call_weather_observed(key, secret, **kwargs)
            if kwargs
            else _call_weather_observed(key, secret)
        )

        # Extract data
        observed_df = _extract_weather_observed(observed_json)

        # Clean data
        observed_gdf = _clean_weather_observed(observed_df)

    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return observed_gdf


def _call_weather_forecast(
    key,
    secret,
    input_type="location",
    location=(-105.648222, 40.313250),
    field_id=None,
    start_date=None,
    end_date=None,
    limit=10,
    offset=0,
    block_size=24,
):
    """
    Retrieves weather forecast data from the
    aWhere API, based on input parameters.
    """
    # Check input data type
    # Location-based
    if input_type == "location":

        # Raise error if location is not defined
        if location is None:
            raise ValueError("Must specify a location (longitude, latitude).")

        # Set URL to location
        api_url = (
            f"https://api.awhere.com/v2/weather/locations/"
            f"{location[1]},{location[0]}"
        )

    # Field-based
    elif input_type == "field":

        # Raise error if field name is not defined
        if field_id is None:
            raise ValueError("Must specify a field name ('test-field').")

        # Set URL to fields
        api_url = f"https://api.awhere.com/v2/weather/fields/{field_id}"

    # Invalid input
    else:
        raise ValueError("Invalid date type. Must be 'location' or 'field'.")

    # Get OAuth token
    auth_token = aw.get_oauth_token(key, secret)

    # Setup the HTTP request headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Define URL variants
    url_no_date = (
        f"{api_url}/forecasts?limit={limit}&offset={offset}"
        f"&blockSize={block_size}"
    )
    url_start_date = (
        f"{api_url}/forecasts/{start_date}?limit={limit}"
        f"&offset={offset}&blockSize={block_size}"
    )
    url_end_date = (
        f"{api_url}/forecasts{end_date}?limit={limit}"
        f"&offset={offset}&blockSize={block_size}"
    )
    url_both_dates = (
        f"{api_url}/forecasts/{start_date},{end_date}"
        f"?limit={limit}&offset={offset}&blockSize={block_size}"
    )

    # Perform the HTTP request to obtain the Forecast for the Field
    # Default - 7-day
    if not (start_date or end_date):
        response = rq.get(url_no_date, headers=auth_headers)

    # Single date - specify start day
    elif start_date and not end_date:
        response = rq.get(url_start_date, headers=auth_headers)

    # Single date - specify end day
    elif end_date and not start_date:
        response = rq.get(url_end_date, headers=auth_headers)

    # Date range
    elif start_date and end_date:
        response = rq.get(url_both_dates, headers=auth_headers)

    # Convert response to json format
    weather_forecast = response.json()

    # Return forecast
    return weather_forecast


def _extract_weather_forecast(forecast, forecast_type="main"):
    """Extract aWhere forecast data and returns
    it in a pandas dataframe.

    forecast_type can be 'main' or 'soil'.
    """
    # Initialize lists to store forecast
    forecast_list = []

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

        # Check forecast type
        # Main forecast
        if forecast_type == "main":

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
            forecast_list.append(forecast_norm)

        # Soil forecast
        elif forecast_type == "soil":

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
            forecast_list.append(soil_multi_index)

        # Invalid forecast type
        else:
            raise ValueError(
                "Invalid forecast type. Must be 'main' or 'soil'."
            )

    # Merge list of dataframes into a single dataframe
    merged = pd.concat(forecast_list)

    # Return merged dataframe
    return merged


def _clean_weather_forecast(df):
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
    # Define global variables
    global FORECAST_COORD_COLS, FORECAST_DROP_COLS, FORECAST_RENAME_MAP

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    # Create copy of input dataframe; prevents altering the original
    df_copy = df.copy()

    # Convert to geodataframe
    gdf = gpd.GeoDataFrame(
        df_copy,
        crs=crs,
        geometry=gpd.points_from_xy(
            df[FORECAST_COORD_COLS[0]], df[FORECAST_COORD_COLS[1]]
        ),
    )

    # Add lat/lon columns to drop columns list
    FORECAST_DROP_COLS += FORECAST_COORD_COLS

    # Drop columns
    gdf.drop(columns=FORECAST_DROP_COLS, axis=1, inplace=True, errors="ignore")

    # Rename columns
    gdf.rename(columns=FORECAST_RENAME_MAP, inplace=True, errors="ignore")

    # Return cleaned up geodataframe
    return gdf


def get_weather_forecast(key, secret, forecast_type="main", kwargs=None):
    """kwargs is a dictionary that provides values beyond the default;
    unpack dictionary if it exists

    kwargs are the parameters to get_data() method

    kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}

    input_type='location' 'field'

    forecast_type : str
        Either 'main' (default) or 'soil'.

    kwargs : dict
        input_type="location",
        location=(-105.648222, 40.313250),
        field_id=None,
        start_date="01-01",
        end_date=None,
        limit=10,
        offset=0,
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Call data
        forecast_json = (
            _call_weather_forecast(key, secret, **kwargs)
            if kwargs
            else _call_weather_forecast(key, secret)
        )

        # Extract data
        forecast_df = _extract_weather_forecast(
            forecast_json, forecast_type=forecast_type
        )

        # Clean data
        forecast_gdf = _clean_weather_forecast(forecast_df)

    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    return forecast_gdf
