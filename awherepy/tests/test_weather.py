"""Tests for the weather module."""

import os
import pytest
import shapely
import geopandas as gpd
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


def test_weather_norms(bear_lake_norms, manchester_vermont_norms):
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


def test_weather_observed(bear_lake_observed, manchester_vermont_observed):
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


def test_weather_forecast(bear_lake_forecast, manchester_vermont_forecast):
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
