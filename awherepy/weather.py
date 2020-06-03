"""
awherepy.weather
================
A module to access and retrieve aWhere weather data.
"""

import requests as rq
from pandas.io.json import json_normalize
import geopandas as gpd
import awherepy as aw

# Define variables data cleaning
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


def _get_weather_norms(
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
        api_url = "https://api.awhere.com/v2/weather/locations/"
        f"{location[1]},{location[0]}"

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
    url_multiple_days = f"{api_url}/norms/"
    f"{start_date},{end_date}?limit={limit}&offset={offset}"

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


def weather_norms(key, secret, kwargs=None):
    """kwargs is a dictionary that provides values beyond the default;
    unpack dictionary if it exists

    kwargs are the parameters to get_data() method

    kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}

    input_type='location' 'field'


    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Get data
        norms_json = (
            _get_weather_norms(key, secret, **kwargs)
            if kwargs
            else _get_weather_norms(key, secret)
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
