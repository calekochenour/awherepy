"""Tests for the models module."""

import os
import pytest
import random
import pandas as pd
import geopandas as gpd
import awherepy.fields as awf
import awherepy.plantings as awp
import awherepy.models as awm


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
def single_model(awhere_api_key, awhere_api_secret):
    """Fixture that returns a dataframe containing a single aWhere model.
    """
    # Get single model
    model = awm.get_models(
        key=awhere_api_key,
        secret=awhere_api_secret,
        model_id=random.choice(awm.MODELS_LIST),
    )

    # Return crop
    return model


@pytest.fixture
def all_models(awhere_api_key, awhere_api_secret):
    """Fixture that returns a dataframe containing all aWhere models.
    """
    # Get all models
    models = awm.get_models(key=awhere_api_key, secret=awhere_api_secret)

    # Return crops
    return models


@pytest.fixture
def single_model_details(awhere_api_key, awhere_api_secret):
    """Fixture that returns two dataframes, one containing base
    details for a single model and one containing stage details for that model.
    """
    # Get details
    base_details, stage_details = awm.get_model_details(
        awhere_api_key,
        awhere_api_secret,
        model_id=random.choice(awm.MODELS_LIST),
    )

    # Return details
    return base_details, stage_details


@pytest.fixture
def all_model_details(awhere_api_key, awhere_api_secret):
    """Fixture that returns two dataframes, one containing all model base
    details and one containing all model stage details.
    """
    # Get details
    base_details, stage_details = awm.get_model_details(
        awhere_api_key, awhere_api_secret
    )

    # Return details
    return base_details, stage_details


@pytest.fixture
def model_results(awhere_api_key, awhere_api_secret):
    """Fixture that creates an aWhere field and planting associated with the
    field, gets the model results, and returns the model results.
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
        "crop": "wheat-hardred",
        "planting_date": "2020-05-01",
        "projected_harvest_date": "2020-09-30",
        "projected_yield_amount": 200,
        "projected_yield_units": "boxes",
    }

    # Create planting
    _ = awp.create_planting(
        awhere_api_key,
        awhere_api_secret,
        field_id="VT-Test",
        planting_info=planting_info,
    )

    # Get model results
    results = awm.get_model_results(
        awhere_api_key,
        awhere_api_secret,
        field_id="VT-Test",
        model_id="WheatHardRedMSU",
    )

    # Return model results
    return results


def test_get_models_single(single_model):
    """Tests the get_models() function with a single model.
    """
    # Test object type
    assert isinstance(single_model, pd.DataFrame)

    # Test dataframe column names
    assert "model_name" in single_model.columns
    assert "model_description" in single_model.columns
    assert "model_type" in single_model.columns
    assert "model_source" in single_model.columns
    assert "model_link" in single_model.columns

    # Test number of records
    assert len(single_model) == 1

    # Test model id
    assert single_model.index[0] in awm.MODELS_LIST


def test_get_models_all(all_models):
    """Tests the get_models() function with all models.
    """
    # Test object type
    assert isinstance(all_models, pd.DataFrame)

    # Test dataframe column names
    assert "model_name" in all_models.columns
    assert "model_description" in all_models.columns
    assert "model_type" in all_models.columns
    assert "model_source" in all_models.columns
    assert "model_link" in all_models.columns

    # Test number of records
    assert len(all_models) == len(awm.MODELS_LIST)

    # Test model ids
    for id in all_models.index.values:
        assert id in awm.MODELS_LIST


def test_get_model_details_single(single_model_details):
    """Tests the get_model_details() function with a single model.
    """
    # Extract details
    base_details, stage_details = single_model_details

    # Base details
    # Test object type
    assert isinstance(base_details, pd.DataFrame)

    # Test dataframe information
    assert "biofix_days" in base_details.columns
    assert "gdd_method" in base_details.columns
    assert "gdd_base_temp_cels" in base_details.columns
    assert "gdd_max_boundary_cels" in base_details.columns
    assert "gdd_min_boundary_cels" in base_details.columns

    # Test number of records
    assert len(base_details) == 1

    # Test model ids
    assert base_details.index[0] in awm.MODELS_LIST

    # Stage details
    # Test object type
    assert isinstance(stage_details, pd.DataFrame)

    # Test dataframe information
    assert "stage_name" in stage_details.columns
    assert "stage_description" in stage_details.columns
    assert "gdd_threshold_cels" in stage_details.columns

    # Test model ids
    assert base_details.index[0] in awm.MODELS_LIST


def test_get_model_details_all(all_model_details):
    """Tests the get_model_details() function with all models.
    """
    # Extract details
    base_details, stage_details = all_model_details

    # Base details
    # Test object type
    assert isinstance(base_details, pd.DataFrame)

    # Test dataframe information
    assert "biofix_days" in base_details.columns
    assert "gdd_method" in base_details.columns
    assert "gdd_base_temp_cels" in base_details.columns
    assert "gdd_max_boundary_cels" in base_details.columns
    assert "gdd_min_boundary_cels" in base_details.columns

    # Test number of records
    assert len(base_details) == 29

    # Test model ids
    for id in base_details.index.values:
        assert id in awm.MODELS_LIST

    # Stage details
    # Test object type
    assert isinstance(stage_details, pd.DataFrame)

    # Test dataframe information
    assert "stage_name" in stage_details.columns
    assert "stage_description" in stage_details.columns
    assert "gdd_threshold_cels" in stage_details.columns

    # Test number of records
    assert len(stage_details) == 307

    # Test model ids
    for model_id, _ in stage_details.index.values:
        assert model_id in awm.MODELS_LIST


def test_get_model_results(model_results):
    """Tests the get_model_results() function.
    """
    # Test object type
    assert isinstance(model_results, gpd.GeoDataFrame)

    # Test geodataframe information
    assert "model_id" in model_results.columns
    assert "biofix_date" in model_results.columns
    assert "planting_date" in model_results.columns
    assert "stage_start_date" in model_results.columns
    assert "stage_id" in model_results.columns
    assert "stage_name" in model_results.columns
    assert "stage_description" in model_results.columns
    assert "gdd_threshold_cels" in model_results.columns
    assert "gdd_accumulation_current_cels" in model_results.columns
    assert "gdd_remaining_next_cels" in model_results.columns
