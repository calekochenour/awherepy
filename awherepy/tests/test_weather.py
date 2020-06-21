"""Tests for the weather module."""

import os
import pytest
from datetime import date, timedelta
import shapely
import geopandas as gpd
import awherepy.fields as awf
import awherepy.weather as aww


@pytest.fixture
def awhere_api_key():
    """Fixture that returns the key used to
    connect to the aWhere API.
    """
    return os.environ.get("AWHERE_API_KEY")


@pytest.fixture
def awhere_api_secret():
    """Fixture that returns the secret used to
    connect to the aWhere API.
    """
    return os.environ.get("AWHERE_API_SECRET")


@pytest.fixture
def manchester_vermont_longitude():
    """Fixture that returns the longitude for Manchester, Vermont.
    """
    return -73.0723269


@pytest.fixture
def manchester_vermont_latitude():
    """Fixture that returns the latitude for Manchester, Vermont.
    """
    return 43.1636875


@pytest.fixture
def bear_lake_norms(awhere_api_key, awhere_api_secret):
    """Fixture that returns a geodataframe for the weather norms,
    with the default parameters.
    """
    return aww.get_weather_norms(key=awhere_api_key, secret=awhere_api_secret)


@pytest.fixture
def manchester_vermont_norms(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe for the weather norms
    for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (
            manchester_vermont_longitude,
            manchester_vermont_latitude,
        ),
        "start_date": "05-10",
        "end_date": "05-20",
    }

    return aww.get_weather_norms(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


@pytest.fixture
def bear_lake_observed(awhere_api_key, awhere_api_secret):
    """Fixture that returns a geodataframe for the observed weather
    for Bear Lake, RMNP, Colorado.
    """
    # Define kwargs for Bear Lake, RMNP, Colorado
    bear_lake_kwargs = {"start_date": "2020-05-10", "end_date": "2020-05-20"}

    return aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=bear_lake_kwargs
    )


@pytest.fixture
def manchester_vermont_observed(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe for the observed weather
    for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (
            manchester_vermont_longitude,
            manchester_vermont_latitude,
        ),
        "start_date": "2020-05-10",
        "end_date": "2020-05-20",
    }

    return aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


@pytest.fixture
def bear_lake_forecast(awhere_api_key, awhere_api_secret):
    """Fixture that returns a geodataframe for the weather forecast,
    with the default parameters.
    """
    return aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret
    )


@pytest.fixture
def manchester_vermont_forecast(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe for the weather forecast
    for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (manchester_vermont_longitude, manchester_vermont_latitude)
    }

    return aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


def test_get_weather_norms(bear_lake_norms, manchester_vermont_norms):
    """Tests the get_weather_norms() function.
    """
    # Weather norms - Bear Lake, RMNP, Colorado (default values)
    # Test object type
    assert isinstance(bear_lake_norms, gpd.GeoDataFrame)

    # Test average temp for Jan-01
    assert round(bear_lake_norms.mean_temp_avg_cels[0], 2) == -14.09

    # Test number of entries in the geodataframe
    assert len(bear_lake_norms) == 1

    # Test geometry type
    assert isinstance(
        bear_lake_norms.iloc[0].geometry, shapely.geometry.polygon.Point
    )

    # Test number of columns
    assert len(bear_lake_norms.columns) == 19

    # Weather norms - Manchester, Vermont
    # Test object type
    assert isinstance(manchester_vermont_norms, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(manchester_vermont_norms) == 10

    # Test geometry type
    assert isinstance(
        manchester_vermont_norms.iloc[0].geometry,
        shapely.geometry.polygon.Point,
    )

    # Test average precip for May 15
    assert (
        round(manchester_vermont_norms.loc["05-15"].precip_avg_mm, 2) == 4.73
    )


def test_get_weather_observed(bear_lake_observed, manchester_vermont_observed):
    """Tests the get_weather_observed() function.
    """
    # Weather observed - Bear Lake, RMNP, Colorado
    # Test object type
    assert isinstance(bear_lake_observed, gpd.geodataframe.GeoDataFrame)

    # Test precip amount
    assert (
        round(bear_lake_observed.loc["2020-05-15"].precip_amount_mm, 2) == 2.40
    )

    # Test number of entries in the geodataframe
    assert len(bear_lake_observed) == 10

    # Test geometry type
    assert isinstance(
        bear_lake_observed.iloc[0].geometry, shapely.geometry.polygon.Point
    )

    # Test number of columns
    assert len(bear_lake_observed.columns) == 10

    # Weather observed - Manchester, Vermont
    # Test object type
    assert isinstance(manchester_vermont_observed, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(manchester_vermont_observed) == 10

    # Test geometry type
    assert isinstance(
        manchester_vermont_observed.iloc[0].geometry,
        shapely.geometry.polygon.Point,
    )

    # Test average precip for May 15
    assert (
        round(
            manchester_vermont_observed.loc["2020-05-15"].precip_amount_mm, 2
        )
        == 25.84
    )


def test_get_weather_forecast(bear_lake_forecast, manchester_vermont_forecast):
    """Tests the get_weather_forecast() function.
    """
    # Weather forecast - Bear Lake, RMNP, Colorado
    # Test object type
    assert isinstance(bear_lake_forecast, gpd.geodataframe.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(bear_lake_forecast) == 10

    # Test geometry type
    assert isinstance(
        bear_lake_forecast.iloc[0].geometry, shapely.geometry.polygon.Point
    )

    # Test number of columns
    assert len(bear_lake_forecast.columns) == 21

    # Weather forecast - Manchester, Vermont
    # Test object type
    assert isinstance(manchester_vermont_forecast, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(manchester_vermont_forecast) == 10

    # Test number of columns
    assert len(manchester_vermont_forecast.columns) == 21

    # Test geometry type
    assert isinstance(
        manchester_vermont_forecast.iloc[0].geometry,
        shapely.geometry.polygon.Point,
    )


def test_get_weather_norms_invalid_location(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_norms() function with a missing location.
    """
    # Define kwargs with invalid location
    kwargs = {
        "location": None,
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test invalid location
    with pytest.raises(
        ValueError,
        match="Must specify a location, with longitude and latitude.",
    ):
        aww.get_weather_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_norms_valid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_norms() function with a valid field.
    """
    # Define field paramaters
    field_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Create field
    try:
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Delete field if already exists
    except KeyError:
        awf.delete_field(
            awhere_api_key,
            awhere_api_secret,
            field_id=field_info.get("field_id"),
        )

        # Create field again
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define kwargs with field
    kwargs = {
        "input_type": "field",
        "field_id": "VT-Test",
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Get weather norms
    norms = aww.get_weather_norms(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(norms, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(norms) == 10


def test_get_weather_norms_invalid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_norms() function with a missing field.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "field",
        "field_id": None,
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test missing field id
    with pytest.raises(ValueError, match="Must specify a field name."):
        aww.get_weather_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_norms_invalid_parameters(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_norms() function with an invalid input type.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "Invalid",
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test missing field id
    with pytest.raises(
        ValueError, match="Invalid input type. Must be 'location' or 'field'."
    ):
        aww.get_weather_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_norms_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_norms() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_norms(key="Invalid-Key", secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_norms(key=awhere_api_key, secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_norms(key="Invalid-Key", secret=awhere_api_secret)


def test_get_weather_observed_invalid_location(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_observed() function with a missing location.
    """
    # Define kwargs with invalid location
    kwargs = {
        "location": None,
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test invalid location
    with pytest.raises(
        ValueError,
        match="Must specify a location, with longitude and latitude.",
    ):
        aww.get_weather_observed(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_observed_valid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_observed() function with a valid field.
    """
    # Define field paramaters
    field_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Create field
    try:
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Delete field if already exists
    except KeyError:
        awf.delete_field(
            awhere_api_key,
            awhere_api_secret,
            field_id=field_info.get("field_id"),
        )

        # Create field again
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define kwargs with field
    kwargs = {
        "input_type": "field",
        "field_id": "VT-Test",
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Get observed weather
    observed = aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(observed, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(observed) == 10


def test_get_weather_observed_invalid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_observed() function with a missing field.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "field",
        "field_id": None,
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test missing field id
    with pytest.raises(ValueError, match="Must specify a field name."):
        aww.get_weather_observed(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_observed_invalid_parameters(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_observed() function with an invalid input type.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "Invalid",
        "start_date": "05-10",
        "end_date": "05-19",
    }

    # Test missing field id
    with pytest.raises(
        ValueError, match="Invalid input type. Must be 'location' or 'field'."
    ):
        aww.get_weather_observed(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_observed_dates(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_observed() function with combinations of date
    parameters (start, end).
    """
    # Get observed weather with no input dates
    observed = aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret
    )

    # Test object type
    assert isinstance(observed, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(observed) == 7

    # Define kwargs with only start date
    kwargs = {
        "start_date": "05-10",
    }

    # Get observed weather with only start date
    observed = aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(observed, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(observed) == 1

    # Define kwargs with only end date
    kwargs = {
        "end_date": "05-19",
    }

    # Get observed weather with only end start date
    observed = aww.get_weather_observed(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(observed, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(observed) == 1


def test_get_weather_observed_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_observed() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_observed(key="Invalid-Key", secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_observed(key=awhere_api_key, secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_observed(key="Invalid-Key", secret=awhere_api_secret)


def test_get_weather_forecast_invalid_location(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_forecast() function with a missing location.
    """
    # Define kwargs with invalid location
    kwargs = {
        "location": None,
    }

    # Test invalid location
    with pytest.raises(
        ValueError,
        match="Must specify a location, with longitude and latitude.",
    ):
        aww.get_weather_forecast(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_forecast_valid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_forecast() function with a valid field.
    """
    # Define field paramaters
    field_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Create field
    try:
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Delete field if already exists
    except KeyError:
        awf.delete_field(
            awhere_api_key,
            awhere_api_secret,
            field_id=field_info.get("field_id"),
        )

        # Create field again
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define kwargs with field
    kwargs = {
        "input_type": "field",
        "field_id": "VT-Test",
    }

    # Get weather forecast
    forecast = aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(forecast, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(forecast) == 10


def test_get_weather_forecast_invalid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_forecast() function with a missing field.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "field",
        "field_id": None,
    }

    # Test missing field id
    with pytest.raises(ValueError, match="Must specify a field name."):
        aww.get_weather_forecast(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_weather_forecast_invalid_parameters(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_forecast() function for expected invalid parameter
    errors/exceptions.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "Invalid",
    }

    # Test missing field id
    with pytest.raises(
        ValueError, match="Invalid input type. Must be 'location' or 'field'."
    ):
        aww.get_weather_forecast(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )

    # Test invalid forecast type
    with pytest.raises(
        ValueError, match="Invalid forecast type. Must be 'main' or 'soil'."
    ):
        aww.get_weather_forecast(
            key=awhere_api_key,
            secret=awhere_api_secret,
            forecast_type="Invalid",
        )


def test_get_weather_forecast_dates(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_forecast() function with combinations of date
    parameters (start, end).
    """
    # Define kwargs with only start date
    kwargs = {
        "start_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
    }

    # Get weather forecast with only start date
    forecast = aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(forecast, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(forecast) == 1

    # Define kwargs with only end date
    kwargs = {
        "end_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
    }

    # Get weather forecast with only end start date
    forecast = aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(forecast, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(forecast) == 1

    # Define kwargs with starts and end dates
    kwargs = {
        "start_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
    }

    # Get weather forecast with only end start date
    forecast = aww.get_weather_forecast(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(forecast, gpd.GeoDataFrame)

    # Test number of entries in the geodataframe
    assert len(forecast) == 10


def test_get_weather_forecast_soil(awhere_api_key, awhere_api_secret):
    """Tests the get_weather_forecast() function with a soil forecast.
    """
    # Get forecast
    forecast = aww.get_weather_forecast(
        awhere_api_key, awhere_api_secret, forecast_type="soil"
    )

    # Test object type
    assert isinstance(forecast, gpd.GeoDataFrame)

    # Test number or records
    assert len(forecast) == 40

    # Test number of columns
    assert len(forecast.columns) == 7


def test_get_weather_forecast_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_weather_forecast() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_forecast(key="Invalid-Key", secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_forecast(key=awhere_api_key, secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        aww.get_weather_forecast(key="Invalid-Key", secret=awhere_api_secret)
