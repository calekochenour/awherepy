# -*- coding: utf-8 -*-
"""Tests for the grid module."""

import os
import pytest

# import shapely

# from shapely.geometry import Polygon
import geopandas as gpd


# import random

# from awherepy import awherepy, grid

import awherepy.grid as ag


# @pytest.fixture
# def generate_numbers():
#     """Sample pytest fixture. Generates list of random integers.
#
#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#
#     return random.sample(range(100), 10)
#
#
# def test_sum_numbers(generate_numbers):
#     """Sample test function for sum_numbers, using pytest fixture."""
#
#     our_result = awherepy.sum_numbers(generate_numbers)
#     assert our_result == sum(generate_numbers)
#
#
# def test_max_number(generate_numbers):
#     """Sample test function for max_number, using pytest fixture."""
#
#     our_result = awherepy.max_number(generate_numbers)
#     assert our_result == max(generate_numbers)


# def test_max_number_bad(generate_numbers):
#     """Sample test function that fails. Uncomment to see."""
#
#     our_result = awherepy.max_number(generate_numbers)
#     assert our_result == max(generate_numbers) + 1


@pytest.fixture
def vermont_grid():
    """Fixture that returns the aWhere grid for
    the state of Vermont.
    """
    # Define path to shapefile boundary
    vt_bound_path = os.path.join("test-data", "vermont_state_boundary.shp")
    # Create aWhere grid and boundary
    vt_grid, vt_bound_4326 = ag.create_grid(
        vt_bound_path, buffer_distance=0.12
    )

    # Return grid
    return vt_grid


@pytest.fixture
def vermont_boundary():
    """Fixture that returns the study area boundary
    for the state of Vermont.
    """
    # Define path to shapefile boundary
    vt_bound_path = os.path.join("test-data", "vermont_state_boundary.shp")
    # Create aWhere grid and boundary
    vt_grid, vt_bound_4326 = ag.create_grid(
        vt_bound_path, buffer_distance=0.12
    )

    # Return grid
    return vt_bound_4326


def test_create_grid(vermont_grid):
    """Test the aWhere grid output for Vermont state
    """
    # Grid should be a geopandas geodataframe
    assert isinstance(vermont_grid, gpd.geodataframe.GeoDataFrame)

    # Grid should have 533 grid cells (polygons)
    assert len(vermont_grid) == 533

    # First grid cell should be a shapely polygons
    # assert isinstance(
    #     vermont_grid.loc[43].geometry, shapely.geometry.polygon.Polygon
    # )

    # # Should fail
    # assert isinstance(
    #     vermont_grid.loc[43].geometry, gpd.geodataframe.GeoDataFrame
    # )

    # def test_extract_centroids():
    #     pass
    #
    #
    # def test_rasterize():
    #     pass
    #
    #
    # def test_plot_grid():
    #     pass
    #
    #
    # def test_export_grid():
    #     pass
