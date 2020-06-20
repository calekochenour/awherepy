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
    try:
        field = awf.create_field(
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


def test_update_field_name(awhere_api_key, awhere_api_secret):
    """Tests the update_field() function, only updating the field name.
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

    # Define update info
    update_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test-Update",
    }

    # Update the field
    field = awf.update_field(
        awhere_api_key, awhere_api_secret, field_info=update_info
    )

    # Test object type
    assert isinstance(field, gpd.GeoDataFrame)

    # Test geodataframe information
    assert field.index == "VT-Test"
    assert field.field_name[0] == "VT-Field-Test-Update"
    assert field.area_acres[0] == 10
    assert field.farm_id[0] == "VT-Farm-Test"

    # Test number of records
    assert len(field) == 1


def test_update_farm_id(awhere_api_key, awhere_api_secret):
    """Tests the update_field() function, only updating the farm id.
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

    # Define update info
    update_info = {
        "field_id": "VT-Test",
        "farm_id": "VT-Farm-Test-Update",
    }

    # Update the field
    field = awf.update_field(
        awhere_api_key, awhere_api_secret, field_info=update_info
    )

    # Test object type
    assert isinstance(field, gpd.GeoDataFrame)

    # Test geodataframe information
    assert field.index == "VT-Test"
    assert field.field_name[0] == "VT-Field-Test"
    assert field.area_acres[0] == 10
    assert field.farm_id[0] == "VT-Farm-Test-Update"

    # Test number of records
    assert len(field) == 1


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


def test_get_fields_invalid_credentials(awhere_api_key, awhere_api_secret):
    """Tests the get_fields() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.get_fields(
            key="Invalid-Key", secret="Invalid-Secret",
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.get_fields(
            key=awhere_api_key, secret="Invalid-Secret",
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.get_fields(
            key="Invalid-Key", secret=awhere_api_secret,
        )


def test_create_field_invalid_credentials(awhere_api_key, awhere_api_secret):
    """Tests the create_field() function for expected invalid API
    credentials errors/exceptions.
    """
    # Define field paramaters
    field_info = {
        "field_id": "VT",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.create_field(
            key="Invalid-Key", secret="Invalid-Secret", field_info=field_info
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.create_field(
            key=awhere_api_key, secret="Invalid-Secret", field_info=field_info
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.create_field(
            key="Invalid-Key", secret=awhere_api_secret, field_info=field_info
        )


def test_update_field_invalid_credentials(awhere_api_key, awhere_api_secret):
    """Tests the update_field() function for expected invalid API
    credentials errors/exceptions.
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

    # Define update info
    update_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test-Update",
        "farm_id": "VT-Farm-Test-Update",
    }

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.update_field(
            key="Invalid-Key", secret="Invalid-Secret", field_info=update_info
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.update_field(
            key=awhere_api_key, secret="Invalid-Secret", field_info=update_info
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.update_field(
            key="Invalid-Key", secret=awhere_api_secret, field_info=update_info
        )


def test_delete_field_invalid_credentials(awhere_api_key, awhere_api_secret):
    """Tests the delete_field() function for expected invalid API
    credentials errors/exceptions.
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

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.delete_field(
            key="Invalid-Key", secret="Invalid-Secret", field_id="VT-Test"
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.delete_field(
            key=awhere_api_key, secret="Invalid-Secret", field_id="VT-Test"
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awf.delete_field(
            key="Invalid-Key", secret=awhere_api_secret, field_id="VT-Test"
        )


def test_create_field_invalid_parameters(awhere_api_key, awhere_api_secret):
    """Tests the create_field() function for expected invalid parameter
    errors/exceptions.
    """
    # Define invalid field paremeter type (list)
    field_info = [
        "VT-Test",
        "VT-Field-Test",
        "VT-Farm-Test",
        43.1636875,
        -73.0723269,
        10,
    ]

    # Test invalid field info type
    with pytest.raises(
        TypeError,
        match=("Invalid type: 'field_info' must be of type dictionary."),
    ):
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define field paramaters missing field id
    field_info = {
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Test missing field id
    with pytest.raises(
        KeyError, match=("Missing required field parameter: 'field_id'.")
    ):
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define field paramaters missing center latitude
    field_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_longitude": -73.0723269,
        "acres": 10,
    }

    # Test missing center latitude
    with pytest.raises(
        KeyError,
        match=("Missing required field parameter: 'center_latitude'."),
    ):
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )

    # Define field paramaters missing center longitude
    field_info = {
        "field_id": "VT-Test",
        "field_name": "VT-Field-Test",
        "farm_id": "VT-Farm-Test",
        "center_latitude": 43.1636875,
        "acres": 10,
    }

    # Test missing center longitude
    with pytest.raises(
        KeyError,
        match=("Missing required field parameter: 'center_longitude'."),
    ):
        awf.create_field(
            awhere_api_key, awhere_api_secret, field_info=field_info
        )


def test_update_field_invalid_parameters(awhere_api_key, awhere_api_secret):
    """Tests the update_field() function for expected invalid parameter
    errors/exceptions.
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

    # Define update info with invalid type (list)
    update_info = [
        "VT-Test",
        "VT-Field-Test-Update",
        "VT-Farm-Test-Update",
    ]

    # Test invalid field info type
    with pytest.raises(
        TypeError,
        match=("Invalid type: 'field_info' must be of type dictionary."),
    ):
        awf.update_field(
            awhere_api_key, awhere_api_secret, field_info=update_info
        )

    # Define update info missing field id
    update_info = {
        "field_name": "VT-Field-Test-Update",
        "farm_id": "VT-Farm-Test-Update",
    }

    # Test missing field id
    with pytest.raises(
        KeyError, match=("Missing required field parameter: 'field_id'.")
    ):
        awf.update_field(
            awhere_api_key, awhere_api_secret, field_info=update_info
        )

    # Define update info missing field name and farm id
    update_info = {
        "field_id": "VT-Test",
    }

    # Test missing field field name and farm id
    with pytest.raises(
        KeyError,
        match=(
            (
                "Missing parameter: must update at least one attribute,"
                "'field_name' or 'farm_id'."
            )
        ),
    ):
        awf.update_field(
            awhere_api_key, awhere_api_secret, field_info=update_info
        )

    # Define update info with invalid field id
    update_info = {
        "field_id": "VT-Invalid",
        "field_name": "VT-Field-Test-Update",
        "farm_id": "VT-Farm-Test-Update",
    }

    # Test invalid field id
    with pytest.raises(
        KeyError, match="Field name does not exist within account."
    ):
        awf.update_field(
            awhere_api_key, awhere_api_secret, field_info=update_info
        )
