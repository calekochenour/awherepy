"""Tests for the fields module."""

import os
import pytest
import geopandas as gpd
import awherepy.fields as awf


@pytest.fixture
def awhere_api_key():
    """Fixture that returns the key used to
    connect to the aWhere API.
    """
    # Get API key from an environmental variable
    api_key = os.environ.get("AWHERE_API_KEY")

    # Return key
    return api_key


@pytest.fixture
def awhere_api_secret():
    """Fixture that returns the secret used to
    connect to the aWhere API.
    """
    # Get API secret from an environmental variable
    api_secret = os.environ.get("AWHERE_API_SECRET")

    # Return key
    return api_secret


@pytest.fixture
def created_field(awhere_api_key, awhere_api_secret):
    """Fixture that creates and returns an aWhere field.
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
    field = awf.create_field(
        awhere_api_key, awhere_api_secret, field_info=field_info
    )

    # Return field
    return field


@pytest.fixture
def retrieved_field(awhere_api_key, awhere_api_secret):
    """Fixture that gets and returns an aWhere field.
    """
    # Get field
    field = awf.get_fields(
        awhere_api_key, awhere_api_secret, kwargs={"field_id": "VT-Test"}
    )

    # Return fields
    return field


@pytest.fixture
def updated_field(awhere_api_key, awhere_api_secret):
    """Fixture that updates the field name and farm id for a field.
    """
    # Define update info
    update_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test-Update",
        "farm_id": "VT-Farm-Test-Update",
    }

    # Update the field
    field = awf.update_field(
        awhere_api_key, awhere_api_secret, field_info=update_info
    )

    # Return updated field
    return field


@pytest.fixture
def deleted_field(awhere_api_key, awhere_api_secret):
    """Fixture that deletes a field and returns the deletion message.
    """
    # Delete message
    output_message = awf.delete_field(
        awhere_api_key, awhere_api_secret, field_id="VT-Test"
    )

    # Return message
    return output_message


def test_create_field(created_field):
    """Tests the create_field() function.
    """
    # Test object type
    assert isinstance(created_field, gpd.GeoDataFrame)

    # Test geodataframe information
    assert created_field.index == "VT-Test"
    assert created_field.field_name[0] == "VT-Field-Test"
    assert created_field.area_acres[0] == 10
    assert created_field.farm_id[0] == "VT-Farm-Test"

    # Test number of records
    assert len(created_field) == 1


def test_get_fields(retrieved_field):
    """Tests the get_fields() function with a single field.
    """
    # Test object type
    assert isinstance(retrieved_field, gpd.GeoDataFrame)

    # Test geodataframe information
    assert retrieved_field.index == "VT-Test"
    assert retrieved_field.field_name[0] == "VT-Field-Test"
    assert retrieved_field.area_acres[0] == 10
    assert retrieved_field.farm_id[0] == "VT-Farm-Test"

    # Test number of records
    assert len(retrieved_field) == 1


def test_update_field(updated_field):
    """Tests the update_field() function.
    """
    # Test object type
    assert isinstance(updated_field, gpd.GeoDataFrame)

    # Test geodataframe information
    assert updated_field.index == "VT-Test"
    assert updated_field.field_name[0] == "VT-Field-Test-Update"
    assert updated_field.area_acres[0] == 10
    assert updated_field.farm_id[0] == "VT-Farm-Test-Update"

    # Test number of records
    assert len(updated_field) == 1


def test_delete_field(awhere_api_key, awhere_api_secret, deleted_field):
    """Tests the delete_field() function.
    """
    # Test output message
    assert deleted_field[:13] == "Deleted field"

    # Test expected error with re-delete error
    with pytest.raises(
        KeyError, match="Field name does not exist within account."
    ):
        awf.delete_field(awhere_api_key, awhere_api_secret, field_id="VT-Test")
