"""Tests for the agronomics module."""

import os
import pytest
from datetime import date, timedelta
import geopandas as gpd
import awherepy.agronomics as awa
import awherepy.fields as awf


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
    """Fixture that returns a geodataframe containing the agronomic norms,
    with the default parameters.
    """
    return awa.get_agronomic_norms(
        key=awhere_api_key, secret=awhere_api_secret
    )


@pytest.fixture
def manchester_vermont_norms(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe containing agronomic norms
    for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (
            manchester_vermont_longitude,
            manchester_vermont_latitude,
        ),
        "start_date": "05-10",
        "end_date": "05-19",
    }

    return awa.get_agronomic_norms(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


@pytest.fixture
def bear_lake_observed(awhere_api_key, awhere_api_secret):
    """Fixture that returns a geodataframe containing the observed agronomic
    values for Bear Lake, RMNP, Colorado.
    """
    # Define kwargs for Bear Lake, RMNP, Colorado
    bear_lake_kwargs = {"start_date": "2020-05-10", "end_date": "2020-05-19"}

    return awa.get_agronomic_values(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=bear_lake_kwargs
    )


@pytest.fixture
def manchester_vermont_observed(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe containing the observed agronomic
    values for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (
            manchester_vermont_longitude,
            manchester_vermont_latitude,
        ),
        "start_date": "2020-05-10",
        "end_date": "2020-05-19",
    }

    return awa.get_agronomic_values(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


@pytest.fixture
def bear_lake_forecast(awhere_api_key, awhere_api_secret):
    """Fixture that returns a geodataframe containing the agronomic forecast,
    with the default parameters.
    """
    # Define kwargs
    bear_lake_kwargs = {
        "start_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
    }

    return awa.get_agronomic_values(
        awhere_api_key, awhere_api_secret, kwargs=bear_lake_kwargs
    )


@pytest.fixture
def manchester_vermont_forecast(
    awhere_api_key,
    awhere_api_secret,
    manchester_vermont_longitude,
    manchester_vermont_latitude,
):
    """Fixture that returns a geodataframe containing the agronomic forecast
    for Manchester, Vermont.
    """
    # Define kwargs for Manchester, Vermont
    vt_kwargs = {
        "location": (
            manchester_vermont_longitude,
            manchester_vermont_latitude,
        ),
        "start_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (date.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
    }

    return awa.get_agronomic_values(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=vt_kwargs
    )


def test_get_agronomic_norms(bear_lake_norms, manchester_vermont_norms):
    """Tests the get_agronomic_norms() function.
    """
    # Bear Lake, Colorado
    # Test object type
    assert isinstance(bear_lake_norms, gpd.GeoDataFrame)

    # Test number of columns
    assert len(bear_lake_norms.columns) == 7

    # Test number of records
    assert len(bear_lake_norms) == 1

    # Manchester, Vermont
    # Extract norms
    total, daily = manchester_vermont_norms

    # Test object type
    assert isinstance(total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(total.columns) == 11

    # Test number of records
    assert len(total) == 1

    # Test object type
    assert isinstance(daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(daily.columns) == 15

    # Test number of records
    assert len(daily) == 10


def test_get_agronomics_values(
    bear_lake_observed,
    manchester_vermont_observed,
    bear_lake_forecast,
    manchester_vermont_forecast,
):
    """Tests the get_agronomic_values() function.
    """
    # Observed
    # Bear Lake, Colorado
    # Extract observed values
    co_observed_total, co_observed_daily = bear_lake_observed

    # Test object type
    assert isinstance(co_observed_total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(co_observed_total.columns) == 7

    # Test number of records
    assert len(co_observed_total) == 1

    # Test object type
    assert isinstance(co_observed_daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(co_observed_daily.columns) == 8

    # Test number of records
    assert len(co_observed_daily) == 10

    # Manchester, Vermont
    # Extract observed values
    vt_observed_total, vt_observed_daily = manchester_vermont_observed

    # Test object type
    assert isinstance(vt_observed_total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(vt_observed_total.columns) == 7

    # Test number of records
    assert len(vt_observed_total) == 1

    # Test object type
    assert isinstance(vt_observed_daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(vt_observed_daily.columns) == 8

    # Test number of records
    assert len(vt_observed_daily) == 10

    # Forecast
    # Bear Lake, Colorado
    # Extract forecast
    co_forecast_total, co_forecast_daily = bear_lake_forecast

    # Test object type
    assert isinstance(co_forecast_total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(co_forecast_total.columns) == 7

    # Test number of records
    assert len(co_forecast_total) == 1

    # Test object type
    assert isinstance(co_forecast_daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(co_forecast_daily.columns) == 8

    # Test number of records
    assert len(co_forecast_daily) == 10

    # Manchester, Vermont
    # Extract forecast
    vt_forecast_total, vt_forecast_daily = manchester_vermont_forecast

    # Test object type
    assert isinstance(vt_forecast_total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(vt_forecast_total.columns) == 7

    # Test number of records
    assert len(vt_forecast_total) == 1

    # Test object type
    assert isinstance(vt_forecast_daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(vt_forecast_daily.columns) == 8

    # Test number of records
    assert len(vt_forecast_daily) == 10


def test_get_argonomic_norms_invalid_location(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_norms() function with a missing location.
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
        awa.get_agronomic_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomic_norms_valid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_agronomic_norms() function with a valid field.
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

    # Get agronomic norms
    total, daily = awa.get_agronomic_norms(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(total.columns) == 11

    # Test number of records
    assert len(total) == 1

    # Test object type
    assert isinstance(daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(daily.columns) == 15

    # Test number of records
    assert len(daily) == 10


def test_get_agronomic_norms_invalid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_agronomic_norms() function with a missing field.
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
        awa.get_agronomic_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomic_norms_invalid_parameters(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_norms() function with an invalid input type.
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
        awa.get_agronomic_norms(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomic_norms_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_norms() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_norms(key="Invalid-Key", secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_norms(key=awhere_api_key, secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_norms(key="Invalid-Key", secret=awhere_api_secret)


def test_get_agronomic_values_invalid_location(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_values() function with a missing location.
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
        awa.get_agronomic_values(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomic_values_valid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_agronomic_values() function with a valid field.
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
        "start_date": "2020-05-10",
        "end_date": "2020-05-19",
    }

    # Get agronomic values
    total, daily = awa.get_agronomic_values(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(total, gpd.GeoDataFrame)

    # Test number of columns
    assert len(total.columns) == 7

    # Test number of records
    assert len(total) == 1

    # Test object type
    assert isinstance(daily, gpd.GeoDataFrame)

    # Test number of columns
    assert len(daily.columns) == 8

    # Test number of records
    assert len(daily) == 10


def test_get_agronomic_values_invalid_field(awhere_api_key, awhere_api_secret):
    """Tests the get_agronomic_values() function with a missing field.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "field",
        "field_id": None,
        "start_date": "2020-05-10",
        "end_date": "2020-05-19",
    }

    # Test missing field id
    with pytest.raises(ValueError, match="Must specify a field name."):
        awa.get_agronomic_values(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomic_values_invalid_parameters(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_values() function with an invalid input type.
    """
    # Define kwargs with invalid field id
    kwargs = {
        "input_type": "Invalid",
        "start_date": "2020-05-10",
        "end_date": "2020-05-19",
    }

    # Test missing field id
    with pytest.raises(
        ValueError, match="Invalid input type. Must be 'location' or 'field'."
    ):
        awa.get_agronomic_values(
            key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
        )


def test_get_agronomics_values_single_day(awhere_api_key, awhere_api_secret):
    """Tests the get_agronomic_values() function with a single day input.
    """
    # Define kwargs with start date only
    kwargs = {"start_date": "2020-05-10"}

    # Get agronomic values
    values = awa.get_agronomic_values(
        key=awhere_api_key, secret=awhere_api_secret, kwargs=kwargs
    )

    # Test object type
    assert isinstance(values, gpd.GeoDataFrame)

    # Test number of columns
    assert len(values.columns) == 4

    # Test number of records
    assert len(values) == 1


def test_get_agronomic_values_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the get_agronomic_values() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_values(key="Invalid-Key", secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_values(key=awhere_api_key, secret="Invalid-Secret")

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awa.get_agronomic_values(key="Invalid-Key", secret=awhere_api_secret)
