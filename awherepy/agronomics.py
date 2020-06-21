"""
awherepy.agronomics
===================
A module to access and retrieve aWhere agronomics data.
"""

import requests as rq
from datetime import date
import pandas as pd
from pandas.io.json import json_normalize
import geopandas as gpd
import awherepy as aw

# Define variables for data cleaning - norms
# Single day
NORMS_SINGLE_DAY_COORD_COLS = ["location.longitude", "location.latitude"]

NORMS_SINGLE_DAY_DROP_COLS = [
    "location.fieldId",
    "pet.units",
    "_links.self.href",
    "_links.curies",
    "_links.awhere:field.href",
]

NORMS_SINGLE_DAY_RENAME_MAP = {
    "gdd.average": "gdd_daily_average_total_cels",
    "gdd.stdDev": "gdd_daily_average_total_std_dev_cels",
    "pet.average": "pet_daily_average_total_mm",
    "pet.stdDev": "pet_daily_average_total_std_dev_mm",
    "ppet.average": "ppet_daily_average_total",
    "ppet.stdDev": "ppet_daily_average_total_std_dev",
}

# Multi-day
NORMS_MULTIPLE_DAY_COORD_COLS = ["longitude", "latitude"]

# Multi-day, total accumulation
NORMS_MULTIPLE_DAY_TOTAL_DROP_COLS = ["precipitation.units", "pet.units"]

NORMS_MULTIPLE_DAY_TOTAL_RENAME_MAP = {
    "gdd.average": "gdd_range_average_total_cels",
    "gdd.stdDev": "gdd_range_average_total_std_dev_cels",
    "precipitation.average": "precip_range_average_total_mm",
    "precipitation.stdDev": "precip_range_average_total_std_dev_mm",
    "pet.average": "pet_range_average_total_mm",
    "pet.stdDev": "pet_range_average_total_std_dev",
    "ppet.average": "ppet_range_daily_average",
    "ppet.stdDev": "ppet_range_daily_average_std_dev",
}

# Multi-day, daily accumulation
NORMS_MULTIPLE_DAY_DAILY_DROP_COLS = [
    "pet.units",
    "accumulatedPrecipitation.units",
    "accumulatedPet.units",
    "_links.self.href",
    "_links.curies",
    "_links.awhere:field.href",
]

NORMS_MULTIPLE_DAY_DAILY_RENAME_MAP = {
    "gdd.average": "gdd_daily_average_cels",
    "gdd.stdDev": "gdd_daily_average_std_dev_cels",
    "pet.average": "pet_daily_average_mm",
    "pet.stdDev": "pet_daily_average_std_dev_mm",
    "ppet.average": "ppet_daliy_average",
    "ppet.stdDev": "ppet_daily_average_std_dev",
    "accumulatedGdd.average": "gdd_rolling_total_average",
    "accumulatedGdd.stdDev": "gdd_rolling_total_average_std_dev",
    "accumulatedPrecipitation.average": "precip_rolling_total_average_mm",
    "accumulatedPrecipitation.stdDev": (
        "precip_rolling_total_average_" "std_dev_mm"
    ),
    "accumulatedPet.average": "pet_rolling_total_average_mm",
    "accumulatedPet.stdDev": "pet_rolling_total_average_std_dev_mm",
    "accumulatedPpet.average": "ppet_rolling_total_average",
    "accumulatedPpet.stdDev": "ppet_rolling_total_average_std_dev",
}

# Define variables for data cleaning - values
# Single day
VALUES_SINGLE_DAY_COORD_COLS = ["location.longitude", "location.latitude"]

VALUES_SINGLE_DAY_DROP_COLS = [
    "location.fieldId",
    "pet.units",
    "_links.self.href",
    "_links.curies",
    "_links.awhere:field.href",
]

VALUES_SINGLE_DAY_RENAME_MAP = {
    "gdd": "gdd_daily_total_cels",
    "ppet": "ppet_daily_total",
    "pet.amount": "pet_daily_total_mm",
}


# Multi-day
VALUES_MULTIPLE_DAY_COORD_COLS = ["longitude", "latitude"]


# Multi-day, total accumulation
VALUES_MULTIPLE_DAY_TOTAL_DROP_COLS = ["precipitation.units", "pet.units"]

VALUES_MULTIPLE_DAY_TOTAL_RENAME_MAP = {
    "gdd": "gdd_range_total_cels",
    "ppet": "ppet_range_total",  # This is accumulation of all daily PPET
    "precipitation.amount": "precip_range_total_mm",
    "pet.amount": "pet_range_total_mm",
}

# Multi-day, daily accumulation
VALUES_MULTIPLE_DAY_DAILY_DROP_COLS = [
    "pet.units",
    "accumulatedPrecipitation.units",
    "accumulatedPet.units",
    "_links.self.href",
    "_links.curies",
    "_links.awhere:field.href",
]

VALUES_MULTIPLE_DAY_DAILY_RENAME_MAP = {
    "gdd": "gdd_daily_total_cels",
    "ppet": "ppet_daily_total",
    "accumulatedGdd": "gdd_rolling_total_cels",
    "accumulatedPpet": "ppet_rolling_total",
    "pet.amount": "pet_daily_total_mm",
    "accumulatedPrecipitation.amount": "precip_rolling_total_mm",
    "accumulatedPet.amount": "pet_rolling_total_mm",
}


def _call_agronomic_norms(
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
    """Retrieves agronomic norms from the aWhere API.
    """
    # Check input data type
    # Location-based
    if input_type == "location":

        # Raise error if location is not defined
        if location is None:
            raise ValueError(
                ("Must specify a location, with longitude " "and latitude.")
            )

        # Set URL to location
        api_url = (
            "https://api.awhere.com/v2/agronomics/locations/"
            f"{location[1]},{location[0]}"
        )

    # Field-based
    elif input_type == "field":

        # Raise error if field name is not defined
        if field_id is None:
            raise ValueError("Must specify a field name.")

        # Set URL to fields
        api_url = f"https://api.awhere.com/v2/agronomics/fields/{field_id}"

    # Invalid input
    else:
        raise ValueError("Invalid input type. Must be 'location' or 'field'.")

    # Get OAuth token
    auth_token = aw.get_oauth_token(key, secret)

    # Setup the HTTP request headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Define URL variants
    url_single_day = f"{api_url}/agronomicnorms/{start_date}"
    url_multiple_days = (
        f"{api_url}/agronomicnorms/{start_date},{end_date}"
        f"?limit={limit}&offset={offset}"
    )

    # Get single day norms or date range
    response = (
        rq.get(url_multiple_days, headers=auth_headers)
        if end_date
        else rq.get(url_single_day, headers=auth_headers)
    )

    # Convert response to json format
    agronomic_norms = response.json()

    # Return norms
    return agronomic_norms


def _extract_agronomic_norms(agronomic_norms):
    """Extracts data from the aWhere agronomic norms
    data in JSON format.

    Returns
    -------
    agronomics_df : pandas dataframe or tuple of dataframes
        Dataframe(s) containing the extracted data. Single-day
        inputs return a single dataframe. Multi-day inputs return
        a tuple of dataframes (total norms, daily norms).
    """
    # Extract lat/lon
    latitude = agronomic_norms.get("location").get("latitude")
    longitude = agronomic_norms.get("location").get("longitude")

    # Check if more than one day
    if agronomic_norms.get("dailyNorms"):

        # DAILY ACCUMULATION NORMS
        # Get daily accumulation norms
        daily_norms = json_normalize(agronomic_norms.get("dailyNorms"))

        # Add lat/lon and set date as index
        daily_norms["latitude"] = latitude
        daily_norms["longitude"] = longitude
        daily_norms.set_index(["day"], inplace=True)

        # TOTAL ACCUMULATION NORMS
        # Get average accumulations through all days
        total_norms = json_normalize(
            agronomic_norms.get("averageAccumulations")
        )

        # Get list of dates, add start/end dates, set date range as index
        dates = [
            entry.get("day") for entry in agronomic_norms.get("dailyNorms")
        ]

        # Populate date columns
        total_norms["date_range"] = f"{dates[0]}/{dates[-1]}"
        total_norms["start_day"] = dates[0]
        total_norms["end_day"] = dates[-1]
        total_norms.set_index(["date_range"], inplace=True)

        # Add lat/lon
        total_norms["latitude"] = latitude
        total_norms["longitude"] = longitude

        # Put dataframes in tuple (total norms, daily norms)
        agronomics_df = (total_norms, daily_norms)

    # Single day
    else:
        agronomics_df = json_normalize(agronomic_norms)
        agronomics_df.set_index(["day"], inplace=True)

    return agronomics_df


def _clean_agronomic_norms(df):
    """Converts dataframe to geodataframe,
    drops unnecessary columns, and renames
    columns.

    Parameters
    ----------
    df : dataframe or tuple of dataframes
        Input dataframe(s).

    Returns
    -------
    gdf : geopandas geodataframe or tuple of geodataframes
        Geodataframe(s) containing the extracted data. Single-day
        inputs return a single geodataframe. Multi-day inputs return
        a tuple of geodataframes (total norms, daily norms).
    """
    # Define global variables
    global NORMS_SINGLE_DAY_COORD_COLS
    global NORMS_SINGLE_DAY_DROP_COLS
    global NORMS_SINGLE_DAY_RENAME_MAP
    global NORMS_MULTIPLE_DAY_COORD_COLS
    global NORMS_MULTIPLE_DAY_TOTAL_DROP_COLS
    global NORMS_MULTIPLE_DAY_TOTAL_RENAME_MAP
    global NORMS_MULTIPLE_DAY_DAILY_DROP_COLS
    global NORMS_MULTIPLE_DAY_DAILY_RENAME_MAP

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    # Check type of input data
    # Pandas dataframe (single-day input)
    if isinstance(df, pd.core.frame.DataFrame):

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                df_copy[NORMS_SINGLE_DAY_COORD_COLS[0]],
                df_copy[NORMS_SINGLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        NORMS_SINGLE_DAY_DROP_COLS += NORMS_SINGLE_DAY_COORD_COLS

        # Drop columns
        gdf.drop(
            columns=NORMS_SINGLE_DAY_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        gdf.rename(
            columns=NORMS_SINGLE_DAY_RENAME_MAP, inplace=True, errors="ignore"
        )

    # Tuple of dataframes (multi-day input)
    elif isinstance(df, tuple):

        # Total accumulation
        # Create copy of input dataframe; prevents altering the original
        total_df_copy = df[0].copy()

        # Convert to geodataframe
        total_gdf = gpd.GeoDataFrame(
            total_df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                total_df_copy[NORMS_MULTIPLE_DAY_COORD_COLS[0]],
                total_df_copy[NORMS_MULTIPLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        NORMS_MULTIPLE_DAY_TOTAL_DROP_COLS += NORMS_MULTIPLE_DAY_COORD_COLS

        # Drop columns
        total_gdf.drop(
            columns=NORMS_MULTIPLE_DAY_TOTAL_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        total_gdf.rename(
            columns=NORMS_MULTIPLE_DAY_TOTAL_RENAME_MAP,
            inplace=True,
            errors="ignore",
        )

        # Daily accumulation
        # Create copy of input dataframe; prevents altering the original
        daily_df_copy = df[1].copy()

        # Convert to geodataframe
        daily_gdf = gpd.GeoDataFrame(
            daily_df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                daily_df_copy[NORMS_MULTIPLE_DAY_COORD_COLS[0]],
                daily_df_copy[NORMS_MULTIPLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        NORMS_MULTIPLE_DAY_DAILY_DROP_COLS += NORMS_MULTIPLE_DAY_COORD_COLS

        # Drop columns
        daily_gdf.drop(
            columns=NORMS_MULTIPLE_DAY_DAILY_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        daily_gdf.rename(
            columns=NORMS_MULTIPLE_DAY_DAILY_RENAME_MAP,
            inplace=True,
            errors="ignore",
        )

        # Put dataframes in tuple (total norms, daily norms)
        gdf = (total_gdf, daily_gdf)

    # Invalid input type
    else:
        # Raise error
        raise TypeError("Invalid input type.")

    # Return cleaned up geodataframe
    return gdf


def get_agronomic_norms(key, secret, kwargs=None):
    """Gets historical agronomic norms data from the aWhere API.

    API reference: https://docs.awhere.com/knowledge-base-docs/agronomics/

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

            input_type: str
                Type of data, agronomics API by geolocation or API by field.
                Valid options include 'location' and 'field'. Default
                value is 'location'.

            location: tuple of float
                Tuple containing the location (longitude, latitude) that the
                API gets data from. For use with the 'location' input_type.
                Default value is (-105.648222, 40.313250), for Bear Lake, CO.

            field_id: str
                Field ID for a valid aWhere field associated with the input API
                key/secret. For use with the 'field' input_type. Default value
                is None.

            start_date: str
                Start date for the agronomic norms data to be retrieved.
                Formatted 'MM-DD'. All days of the year are valid, from
                '01-01' to '12-31'. Default value is '01-01'.

            end_date: str
                End date for the agronomic norms data to be retrieved.
                Formatted 'MM-DD'. All days of the year are valid, from
                '01-01' to '12-31'. Default value is None.

            limit: int
                Number of results in the API response per page. Used with
                offset kwarg to sort through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Maximum value is 10. Default
                value is 10.

            offset: int
                Number of results in the API response to skip. Used with limit
                kwarg to sort through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Default value is 0 (start
                with first result).

    Returns
    -------
    norms_gdf : geopandas geodataframe or tuple of geodataframes
        Geotdataframe(s) containing the historical agronomic norms
        data for the specified location or aWhere field, for the
        specified date(s). Single-day inputs return a single
        geodataframe. Multi-day inputs return a tuple of geodataframes
        (total norms, daily norms).

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.agronomics as awa
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get historical norms with default kwargs (Bear Lake, CO)
        >>> bear_lake_norms = awa.get_agronomic_norms(
        ...     key=awhere_api_key, secret=awhere_api_secret)
        >>> # Check number of entries in geodataframe
        >>> len(bear_lake_norms)
        1
        >>> # Define non-default kwargs (Manchester Center, Vermont)
        >>> # Define kwargs for Manchester, Vermont
        >>> vt_kwargs = {
        ...     'location': (-73.0723269, 43.1636875),
        ...     'start_date': '05-10',
        ...     'end_date': '05-19'
        ... }
        >>> # Get historical norms for Manchester, Vermont
        >>> vt_total_norms, vt_daily_norms = awa.get_agronomic_norms(
        ...     key=awhere_api_key,
        ...     secret=awhere_api_secret,
        ...     kwargs=vt_kwargs
        ... )
        >>> # Check number entries in geodataframe
        >>> len(vt_total_norms)
        10
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Call data
        norms_json = (
            _call_agronomic_norms(key, secret, **kwargs)
            if kwargs
            else _call_agronomic_norms(key, secret)
        )

        # Extract data
        norms_df = _extract_agronomic_norms(norms_json)

        # Clean data
        norms_gdf = _clean_agronomic_norms(norms_df)

    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return cleaned data
    return norms_gdf


def _call_agronomic_values(
    key,
    secret,
    input_type="location",
    location=(-105.648222, 40.313250),
    field_id=None,
    start_date=date.today().strftime("%m-%d"),
    end_date=None,
    limit=10,
    offset=0,
):
    """Retrieves agronomic values (forecast or observed)
    from the aWhere API.
    """
    # Check input data type
    # Location-based
    if input_type == "location":

        # Raise error if location is not defined
        if location is None:
            raise ValueError(
                ("Must specify a location, with longitude " "and latitude.")
            )

        # Set URL to location
        api_url = (
            "https://api.awhere.com/v2/agronomics/locations/"
            f"{location[1]},{location[0]}"
        )

    # Field-based
    elif input_type == "field":

        # Raise error if field name is not defined
        if field_id is None:
            raise ValueError("Must specify a field name.")

        # Set URL to fields
        api_url = f"https://api.awhere.com/v2/agronomics/fields/{field_id}"

    # Invalid input
    else:
        raise ValueError("Invalid input type. Must be 'location' or 'field'.")

    # Get OAuth token
    auth_token = aw.get_oauth_token(key, secret)

    # Setup the HTTP request headers
    auth_headers = {"Authorization": f"Bearer {auth_token}"}

    # Define URL variants
    url_single_day = f"{api_url}/agronomicvalues/{start_date}"
    url_multiple_days = (
        f"{api_url}/agronomicvalues/{start_date},{end_date}"
        f"?limit={limit}&offset={offset}"
    )

    # Get single day norms or date range
    response = (
        rq.get(url_multiple_days, headers=auth_headers)
        if end_date
        else rq.get(url_single_day, headers=auth_headers)
    )

    # Convert response to json format
    agronomic_values = response.json()

    # Return norms
    return agronomic_values


def _extract_agronomic_values(agronomic_values):
    """Extracts data from the aWhere agronomic forecast
    data in JSON format.

    Returns
    -------
    agronomics_df : pandas dataframe or tuple of dataframes
        Dataframe(s) containing the extracted data. Single-day
        inputs return a single dataframe. Multi-day inputs return
        a tuple of dataframes (total norms, daily norms).
    """
    # Extract lat/lon
    latitude = agronomic_values.get("location").get("latitude")
    longitude = agronomic_values.get("location").get("longitude")

    # Check if more than one day
    if agronomic_values.get("dailyValues"):

        # DAILY ACCUMULATIONS
        # Get daily forecasted accumulations
        daily_accumulation = json_normalize(
            agronomic_values.get("dailyValues")
        )

        # Add lat/lon and set date as index
        daily_accumulation["latitude"] = latitude
        daily_accumulation["longitude"] = longitude
        daily_accumulation.set_index(["date"], inplace=True)

        # TOTAL ACCUMULATION
        # Get total forecasted accumulations through all days
        total_accumulation = json_normalize(
            agronomic_values.get("accumulations")
        )

        # Get list of dates, add start/end dates, set date range as index
        dates = [
            entry.get("date") for entry in agronomic_values.get("dailyValues")
        ]

        # Populate date columns
        total_accumulation["date_range"] = f"{dates[0]}/{dates[-1]}"
        total_accumulation["start_day"] = dates[0]
        total_accumulation["end_day"] = dates[-1]
        total_accumulation.set_index(["date_range"], inplace=True)

        # Add lat/lon
        total_accumulation["latitude"] = latitude
        total_accumulation["longitude"] = longitude

        # Put dataframes in tuple (total accumulation, daily accumulation)
        agronomics_df = (total_accumulation, daily_accumulation)

    # Single day
    else:
        agronomics_df = json_normalize(agronomic_values)
        agronomics_df.set_index(["date"], inplace=True)

    return agronomics_df


def _clean_agronomic_values(df):
    """Converts dataframe to geodataframe,
    drops unnecessary columns, and renames
    columns.

    Parameters
    ----------
    df : dataframe or tuple of dataframes
        Input dataframe(s).

    Returns
    -------
    gdf : geopandas geodataframe or tuple of geodataframes
        Geodataframe(s) containing the extracted data. Single-day
        inputs return a single geodataframe. Multi-day inputs return
        a tuple of geodataframes (total value, daily values).
    """
    # Define global variables
    global VALUES_SINGLE_DAY_COORD_COLS
    global VALUES_SINGLE_DAY_DROP_COLS
    global VALUES_SINGLE_DAY_RENAME_MAP
    global VALUES_MULTIPLE_DAY_COORD_COLS
    global VALUES_MULTIPLE_DAY_TOTAL_DROP_COLS
    global VALUES_MULTIPLE_DAY_TOTAL_RENAME_MAP
    global VALUES_MULTIPLE_DAY_DAILY_DROP_COLS
    global VALUES_MULTIPLE_DAY_DAILY_RENAME_MAP

    # Define CRS (EPSG 4326)
    crs = "epsg:4326"

    # Check type of input data
    # Pandas dataframe (single-day input)
    if isinstance(df, pd.core.frame.DataFrame):

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                df_copy[VALUES_SINGLE_DAY_COORD_COLS[0]],
                df_copy[VALUES_SINGLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        VALUES_SINGLE_DAY_DROP_COLS += VALUES_SINGLE_DAY_COORD_COLS

        # Drop columns
        gdf.drop(
            columns=VALUES_SINGLE_DAY_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        gdf.rename(
            columns=VALUES_SINGLE_DAY_RENAME_MAP, inplace=True, errors="ignore"
        )

    # Tuple of dataframes (multi-day input)
    elif isinstance(df, tuple):

        # Total accumulation
        # Create copy of input dataframe; prevents altering the original
        total_df_copy = df[0].copy()

        # Convert to geodataframe
        total_gdf = gpd.GeoDataFrame(
            total_df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                total_df_copy[VALUES_MULTIPLE_DAY_COORD_COLS[0]],
                total_df_copy[VALUES_MULTIPLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        VALUES_MULTIPLE_DAY_TOTAL_DROP_COLS += VALUES_MULTIPLE_DAY_COORD_COLS

        # Drop columns
        total_gdf.drop(
            columns=VALUES_MULTIPLE_DAY_TOTAL_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        total_gdf.rename(
            columns=VALUES_MULTIPLE_DAY_TOTAL_RENAME_MAP,
            inplace=True,
            errors="ignore",
        )

        # Daily accumulation
        # Create copy of input dataframe; prevents altering the original
        daily_df_copy = df[1].copy()

        # Convert to geodataframe
        daily_gdf = gpd.GeoDataFrame(
            daily_df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                daily_df_copy[VALUES_MULTIPLE_DAY_COORD_COLS[0]],
                daily_df_copy[VALUES_MULTIPLE_DAY_COORD_COLS[1]],
            ),
        )

        # Add lat/lon columns to drop columns list
        VALUES_MULTIPLE_DAY_DAILY_DROP_COLS += VALUES_MULTIPLE_DAY_COORD_COLS

        # Drop columns
        daily_gdf.drop(
            columns=VALUES_MULTIPLE_DAY_DAILY_DROP_COLS,
            axis=1,
            inplace=True,
            errors="ignore",
        )

        # Rename columns
        daily_gdf.rename(
            columns=VALUES_MULTIPLE_DAY_DAILY_RENAME_MAP,
            inplace=True,
            errors="ignore",
        )

        # Put dataframes in tuple (total norms, daily norms)
        gdf = (total_gdf, daily_gdf)

    # Invalid input type
    else:
        # Raise error
        raise TypeError("Invalid input type.")

    # Return cleaned up geodataframe
    return gdf


def get_agronomic_values(key, secret, kwargs=None):
    """Gets historical agronomic values (forecast and observed)
    data from the aWhere API.

    API reference: https://docs.awhere.com/knowledge-base-docs/agronomics/

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

            input_type: str
                Type of data, agronomics API by geolocation or API by field.
                Valid options include 'location' and 'field'. Default
                value is 'location'.

            location: tuple of float
                Tuple containing the location (longitude, latitude) that the
                API gets data from. For use with the 'location' input_type.
                Default value is (-105.648222, 40.313250), for Bear Lake, CO.

            field_id: str
                Field ID for a valid aWhere field associated with the input API
                key/secret. For use with the 'field' input_type. Default value
                is None.

            start_date: str
                Start date for the agronomic values data to be retrieved.
                Formatted 'YYYY-MM-DD'. All days of the year are valid,
                from 'YYYY-01-01' to 'YYYY-12-31'. Default value is the
                current day.

            end_date: str
                End date for the agronomic values data to be retrieved.
                Formatted 'MM-DD'. All days of the year are valid, from
                'YYYY-01-01' to 'YYYY-12-31'. Default value is None.

            limit: int
                Number of results in the API response per page. Used with
                offset kwarg to sort through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Maximum value is 10. Default
                value is 10.

            offset: int
                Number of results in the API response to skip. Used with limit
                kwarg to sort through pages of results (cases where the
                number of results exceeds the limit per page). Applicable when
                the number of results exceeds 1. Default value is 0 (start
                with first result).

    Returns
    -------
    values_gdf : geopandas geodataframe or tuple of geodataframes
        Geotdataframe(s) containing the agronomics data (forecast
        or observed) data for the specified location or aWhere field,
        for the specified date(s). Single-day inputs return a single
        geodataframe. Multi-day inputs return a tuple of geodataframes
        (total values, daily values).

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> import awherepy.agronomics as awa
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get historical norms with default kwargs (Bear Lake, CO)
        >>> bear_lake_values = awa.get_agronomic_values(
        ...     key=awhere_api_key, secret=awhere_api_secret)
        >>> # Check number of entries in geodataframe
        >>> len(bear_lake_norms)
        1
        >>> # Define non-default kwargs (Manchester Center, Vermont)
        >>> # Define kwargs for Manchester, Vermont
        >>> vt_kwargs = {
        ...     'location': (-73.0723269, 43.1636875),
        ...     'start_date': '2020-05-10',
        ...     'end_date': '2020-05-19'
        ... }
        >>> # Get historical norms for Manchester, Vermont
        >>> vt_total_values, vt_daily_values = awa.get_agronomic_values(
        ...     key=awhere_api_key,
        ...     secret=awhere_api_secret,
        ...     kwargs=vt_kwargs
        ... )
        >>> # Check number entries in geodataframe
        >>> len(vt_total_norms)
        10
    """
    # Check if credentials are valid
    if aw.valid_credentials(key, secret):

        # Call data
        values_json = (
            _call_agronomic_values(key, secret, **kwargs)
            if kwargs
            else _call_agronomic_values(key, secret)
        )

        # Extract data
        values_df = _extract_agronomic_values(values_json)

        # Clean data
        values_gdf = _clean_agronomic_values(values_df)

    else:
        # Raise error
        raise ValueError("Invalid aWhere API credentials.")

    # Return cleaned data
    return values_gdf
