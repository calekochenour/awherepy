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
    try:
        _ = awf.create_field(
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
def updated_planting_partial(
    awhere_api_key, awhere_api_secret, retrieved_planting
):
    """Fixture that updates some planting information for a field.
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
def updated_planting_full(
    awhere_api_key, awhere_api_secret, retrieved_planting
):
    """Fixture that updates all planting information for a field.
    """
    # Define update info
    planting_update_info = {
        "field_id": "VT-Test",
        "planting_id": retrieved_planting.index[0],
        "update_type": "full",
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


def test_update_planting_partial(updated_planting_partial):
    """Tests the update_planting() function with a partial update.

    Updating a planting is not currently available in the
    aWhere API. This test passes by receiving a failure to
    update notification from the API. The function was put in
    place to work with future iterations of the aWhere API.
    """
    # Test expected failure message
    updated_planting_partial == "Failed to update planting."


def test_update_planting_full(updated_planting_full):
    """Tests the update_planting() function with a partial update.

    Updating a planting is not currently available in the
    aWhere API. This test passes by receiving a failure to
    update notification from the API. The function was put in
    place to work with future iterations of the aWhere API.
    """
    # Test expected failure message
    updated_planting_full == "Failed to update planting."


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


def test_create_planting_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the create_plantings() function for expected invalid API
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

    # Define planting parameters
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.create_planting(
            key="Invalid-Key",
            secret="Invalid-Secret",
            field_id="VT-Test",
            planting_info=planting_info,
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.create_planting(
            key=awhere_api_key,
            secret="Invalid-Secret",
            field_id="VT-Test",
            planting_info=planting_info,
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.create_planting(
            key="Invalid-Key",
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )


def test_create_planting_invalid_parameters(awhere_api_key, awhere_api_secret):
    """Tests the create_planting() function for expected invalid
    parameter errors/exceptions.
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

    # Define invalid planting parameters type (list)
    planting_info = [
        random.choice(awc.CROPS_LIST),
        "2020-05-01",
        "2020-09-30",
        200,
        "boxes",
    ]

    # Test invalid planting parameters type
    with pytest.raises(
        TypeError,
        match="Invalid type: 'planting_info' must be of type dictionary.",
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters missing crop
    planting_info = {
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Test planting parameters missing crop
    with pytest.raises(
        KeyError, match="Missing required planting parameter: 'crop'."
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters missing planting date
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Test planting parameters missing crop
    with pytest.raises(
        KeyError, match="Missing required planting parameter: 'planting_date'."
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters with projected yield amount but not units
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
    }

    # Test planting parameters with projected yield amount but not units
    with pytest.raises(
        KeyError,
        match="Missing required planting parameter: 'projected_yield_units'.",
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters with projected yield units but not amount
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_units": "boxes",
    }

    # Test planting parameters with projected yield amount but not units
    with pytest.raises(
        KeyError,
        match="Missing required planting parameter: 'projected_yield_amount'.",
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters with actual yield amount but not units
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "yield_amount": 200,
    }

    # Test planting parameters with actual yield amount but not units
    with pytest.raises(
        KeyError, match="Missing required planting parameter: 'yield_units'."
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )

    # Define planting parameters with actual yield units but not amount
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "yield_units": "boxes",
    }

    # Test planting parameters with actual yield amount but not units
    with pytest.raises(
        KeyError, match="Missing required planting parameter: 'yield_amount'."
    ):
        awp.create_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_info=planting_info,
        )


def test_get_plantings_invalid_credentials(awhere_api_key, awhere_api_secret):
    """Tests the get_plantings() function for expected invalid API
    credentials errors/exceptions.
    """
    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.get_plantings(
            key="Invalid-Key", secret="Invalid-Secret",
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.get_plantings(
            key=awhere_api_key, secret="Invalid-Secret",
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.get_plantings(
            key="Invalid-Key", secret=awhere_api_secret,
        )


def test_get_planting_field_id(awhere_api_key, awhere_api_secret):
    """Tests the get_plantings() function for expected invalid parameter
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

    # Define planting parameters
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Create planting
    awp.create_planting(
        key=awhere_api_key,
        secret=awhere_api_secret,
        field_id="VT-Test",
        planting_info=planting_info,
    )

    # Get planting
    planting = awp.get_plantings(
        key=awhere_api_key,
        secret=awhere_api_secret,
        kwargs={"field_id": "VT-Test"},
    )

    # Test object type
    assert isinstance(planting, pd.DataFrame)

    # Test dataframe information
    assert planting.iloc[0].field_id == "VT-Test"
    assert planting.iloc[0].planting_date == "2020-05-01"
    assert planting.iloc[0].yield_amount_projected == 200
    assert planting.iloc[0].yield_amount_projected_units == "boxes"
    assert planting.iloc[0].harvest_date_projected == "2020-09-30"

    # Test number of records
    assert len(planting) == 1


def test_update_planting_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the update_planting() function for expected invalid API
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

    # Define update info
    planting_update_info = {
        "field_id": "VT-Test",
        "planting_id": planting.index[0],
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

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.update_planting(
            key="Invalid-Key",
            secret="Invalid-Secret",
            planting_info=planting_update_info,
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.update_planting(
            key=awhere_api_key,
            secret="Invalid-Secret",
            planting_info=planting_update_info,
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.update_planting(
            key="Invalid-Key",
            secret=awhere_api_secret,
            planting_info=planting_update_info,
        )


def test_update_planting_invalid_parameters(awhere_api_key, awhere_api_secret):
    """Tests the update_planting() function for expected invalid parameter
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

    # Define update info with invalid field id
    planting_update_info = {
        "field_id": "VT-Invalid",
        "planting_id": planting.index[0],
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

    # Test invalid field id
    with pytest.raises(KeyError, match="Field does not exist within account."):
        awp.update_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            planting_info=planting_update_info,
        )

    # Define update info with invalid planting id
    planting_update_info = {
        "field_id": "VT-Test",
        "planting_id": "Invalid-Planting",
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

    # Test invalid planting id
    with pytest.raises(
        KeyError, match="Planting does not exist within account."
    ):
        awp.update_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            planting_info=planting_update_info,
        )

    # Define update info with invalid update type
    planting_update_info = {
        "field_id": "VT-Test",
        "planting_id": planting.index[0],
        "update_type": "Invalid",
        "crop": "sugarbeet-generic",
        "planting_date": "2020-06-05",
        "projections_yield_amount": 50,
        "projections_yield_units": "large boxes",
        "projected_harvest_date": "2020-08-08",
        "yield_amount": 200,
        "yield_units": "large boxes",
        "harvest_date": "2020-07-31",
    }

    # Test invalid update type
    with pytest.raises(
        ValueError, match="Invalid update type. Must be 'full' or 'partial'."
    ):
        awp.update_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            planting_info=planting_update_info,
        )


def test_delete_planting_invalid_credentials(
    awhere_api_key, awhere_api_secret
):
    """Tests the delete_planting() function for expected invalid API
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

    # Define planting parameters
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Create planting
    awp.create_planting(
        awhere_api_key,
        awhere_api_secret,
        field_id="VT-Test",
        planting_info=planting_info,
    )

    # Test invalid API credentials
    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.delete_planting(
            key="Invalid-Key", secret="Invalid-Secret", field_id="VT-Test"
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.delete_planting(
            key=awhere_api_key, secret="Invalid-Secret", field_id="VT-Test",
        )

    with pytest.raises(ValueError, match="Invalid aWhere API credentials."):
        awp.delete_planting(
            key="Invalid-Key", secret=awhere_api_secret, field_id="VT-Test",
        )


def test_delete_planting_invalid_parameters(awhere_api_key, awhere_api_secret):
    """Tests the delete_planting() function for expected invalid parameter
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

    # Define planting parameters
    planting_info = {
        "crop": random.choice(awc.CROPS_LIST),
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Create planting
    awp.create_planting(
        awhere_api_key,
        awhere_api_secret,
        field_id="VT-Test",
        planting_info=planting_info,
    )

    # Test invalid field id
    with pytest.raises(KeyError, match="Field does not exist within account."):
        awp.delete_planting(
            key=awhere_api_key, secret=awhere_api_secret, field_id="VT-Invalid"
        )

    with pytest.raises(
        KeyError, match="Planting does not exist within account."
    ):
        awp.delete_planting(
            key=awhere_api_key,
            secret=awhere_api_secret,
            field_id="VT-Test",
            planting_id="Invalid-Planting",
        )
