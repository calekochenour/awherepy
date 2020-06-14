"""Tests for the crops module."""

import os
import pytest
import random
import pandas as pd
import awherepy.crops as awc


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
def single_crop(awhere_api_key, awhere_api_secret):
    """Fixture that returns a dataframe containing a single aWhere crop.
    """
    # Get single crop
    crop = awc.get_crops(
        key=awhere_api_key,
        secret=awhere_api_secret,
        crop_id=random.choice(awc.CROPS_LIST),
    )

    # Return crop
    return crop


@pytest.fixture
def all_crops(awhere_api_key, awhere_api_secret):
    """Fixture that returns a dataframe containing all aWhere crops.
    """
    # Get all crops
    crops = awc.get_crops(key=awhere_api_key, secret=awhere_api_secret)

    # Return crops
    return crops


def test_get_crops_single(single_crop):
    """Tests the get_crops() function with a single crop.
    """
    # Test object type
    assert isinstance(single_crop, pd.DataFrame)

    # Test dataframe column names
    assert "crop_id" in single_crop.columns
    assert "crop_name" in single_crop.columns
    assert "crop_type" in single_crop.columns
    assert "crop_variety" in single_crop.columns
    assert "default_crop" in single_crop.columns

    # Test number of records
    assert len(single_crop) == 1

    # Test crop id
    assert single_crop.crop_id[0] in awc.CROPS_LIST


def test_get_crops_all(all_crops):
    """Tests the get_crops() function with all crops.
    """
    # Test object type
    assert isinstance(all_crops, pd.DataFrame)

    # Test dataframe column names
    assert "crop_id" in all_crops.columns
    assert "crop_name" in all_crops.columns
    assert "crop_type" in all_crops.columns
    assert "crop_variety" in all_crops.columns
    assert "default_crop" in all_crops.columns

    # Test number of records
    assert len(all_crops) == len(awc.CROPS_LIST)

    # Test crop ids
    for id in all_crops.crop_id:
        assert id in awc.CROPS_LIST
