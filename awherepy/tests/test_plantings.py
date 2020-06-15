"""Tests for the plantings module."""

import os
import pytest
import random
import pandas as pd
import awherepy.crops as awc
import awherepy.fields as awf
import awherepy.plantings as awp


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
def created_planting(awhere_api_key, awhere_api_secret):
    """Fixture that creates an aWhere field and planting
    associated with the field, and returns the planting
    information.
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
    _ = awf.create_field(
        awhere_api_key, awhere_api_secret, field_info=field_info
    )

    # Define planting parameters
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Create planting
    planting = awp.create_planting(
        awhere_api_key,
        awhere_api_secret,
        field_id="VT-Test",
        planting_info=planting_info,
    )

    # Return planting
    return planting


@pytest.fixture
def retrieved_planting(awhere_api_key, awhere_api_secret):
    """Fixture that gets and returns the most recent aWhere planting.
    """
    # Get planting
    planting = awp.get_plantings(
        awhere_api_key, awhere_api_secret, kwargs={"planting_id": "current"}
    )

    # Return planting
    return planting


@pytest.fixture
def updated_planting(awhere_api_key, awhere_api_secret, retrieved_planting):
    """Fixture that updates the planting information for a field.
    """
    # Define update info
    planting_update_info = {
        "field_id": "VT-Test",
        "planting_id": retrieved_planting.index[0],
        "update_type": "partial",
        "crop": "sugarbeet-generic",
        "planting_date": "2020-06-05",
        "projections_yield_amount": 50,
        "projections_yield_units": "large boxes",
        "projected_harvest_date": "2020-08-08",
        "yield_amount": 200,
        "yield_units": "large boxes",
        "harvest_date": "2020-07-31",
    }

    # Update planting
    planting = awp.update_planting(
        awhere_api_key, awhere_api_secret, planting_info=planting_update_info
    )

    # Return updated planting
    return planting


@pytest.fixture
def deleted_planting(awhere_api_key, awhere_api_secret):
    """Fixture that deletes a planting and returns the deletion message.

    Updating a planting is not currently available in the
    aWhere API. This test passes by receiving a failure to
    update notification from the API. The function was put in
    place to work with future iterations of the aWhere API.
    """
    # Delete message
    output_message = awp.delete_planting(
        awhere_api_key, awhere_api_secret, field_id="VT-Test"
    )

    # Return message
    return output_message


def test_create_planting(created_planting):
    """Tests the create_planting() function.
    """
    # Test object type
    assert isinstance(created_planting, pd.DataFrame)

    # Test dataframe information
    assert created_planting.iloc[0].field_id == "VT-Test"
    assert created_planting.iloc[0].planting_date == "2020-05-01"
    assert created_planting.iloc[0].yield_amount_projected == 200
    assert created_planting.iloc[0].yield_amount_projected_units == "boxes"
    assert created_planting.iloc[0].harvest_date_projected == "2020-09-30"

    # Test number of records
    assert len(created_planting) == 1


def test_get_plantings(retrieved_planting):
    """Tests the get_plantings() function with the most recent planting.
    """
    # Test object type
    assert isinstance(retrieved_planting, pd.DataFrame)

    # Test dataframe information
    assert retrieved_planting.iloc[0].field_id == "VT-Test"
    assert retrieved_planting.iloc[0].planting_date == "2020-05-01"
    assert retrieved_planting.iloc[0].yield_amount_projected == 200
    assert retrieved_planting.iloc[0].yield_amount_projected_units == "boxes"
    assert retrieved_planting.iloc[0].harvest_date_projected == "2020-09-30"

    # Test number of records
    assert len(retrieved_planting) == 1


def test_update_planting(updated_planting):
    """Tests the update_planting() function.

    Updating a planting is not currently available in the
    aWhere API. This test passes by receiving a failure to
    update notification from the API. The function was put in
    place to work with future iterations of the aWhere API.
    """
    # Test expected failure message
    updated_planting == "Failed to update planting."


def test_delete_planting(awhere_api_key, awhere_api_secret, deleted_planting):
    """Tests the delete_planting() function.
    """
    # Test output message
    assert deleted_planting[:16] == "Deleted planting"

    # Test expected error with retrieving deleted planting
    with pytest.raises(KeyError):
        awp.get_plantings(
            awhere_api_key,
            awhere_api_secret,
            kwargs={"planting_id": "current"},
        )

    # Delete test field after tests
    awf.delete_field(awhere_api_key, awhere_api_secret, field_id="VT-Test")
