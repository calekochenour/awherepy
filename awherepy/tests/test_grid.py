"""Tests for the grid module."""

import os
import pytest
import shapely
import geopandas as gpd
import awherepy.grid as ag


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


@pytest.fixture
def vermont_centroids(vermont_grid):
    """Fixture that returns the centroids from
    the Vermont aWhere grid cells.
    """
    # Extract centroids
    vt_centroids = ag.extract_centroids(vermont_grid)

    # Return centroids
    return vt_centroids


@pytest.fixture
def vermont_population(vermont_grid):
    """Fixture that returns 100x100 meter population
    grid rasterized to the Vermont aWhere grid (9x9 km).
    """
    # Define path to Vermont 2020 population per pixel
    vt_pop_path = os.path.join("test-data", "vt_ppp_2020.tif")

    # Rasterize ppp data (100x100 m) to aWhere grid (9x9 km)
    vt_pop_rasterized = ag.rasterize(vermont_grid, vt_pop_path)

    # Return geodataframe with rasterized pop data
    return vt_pop_rasterized


def test_create_grid(vermont_grid, vermont_boundary):
    """Test the aWhere grid output and study area
    boundary for Vermont.
    """
    # Grid should be a geopandas geodataframe
    assert isinstance(vermont_grid, gpd.geodataframe.GeoDataFrame)

    # Grid should have 533 grid cells (polygons)
    assert len(vermont_grid) == 533

    # First grid cell should be a shapely polygons
    assert isinstance(
        vermont_grid.loc[43].geometry, shapely.geometry.polygon.Polygon
    )

    # Boundary should be a geopandas geodataframe
    assert isinstance(vermont_boundary, gpd.geodataframe.GeoDataFrame)

    # Boundary should have one polygon
    assert len(vermont_boundary) == 1

    # GEOID should be '50'
    assert vermont_boundary.loc[0]["STATEGEOID"] == "50"

    # Grid and boundary CRS should match
    assert vermont_grid.crs == vermont_boundary.crs


def test_extract_centroids(vermont_centroids):
    """Test the extracted aWhere grid centroids
    for Vermont.
    """
    # Number of centroids (grid cells)
    assert len(vermont_centroids) == 533

    # First centroid
    assert vermont_centroids[0] == (-73.43783985107041, 43.52701241643375)

    # Last centroid
    assert vermont_centroids[-1] == (-71.43783985107045, 45.047012416433724)


def test_rasterize(vermont_population):
    """Test aWhere-rasterized ppp data for Vermont.
    """
    # Grid should be a geopandas geodataframe
    assert isinstance(vermont_population, gpd.geodataframe.GeoDataFrame)

    # Population sum column should be in geodataframe
    assert "sum" in vermont_population.columns

    # Number of 100x100 m cells rasterized to aWhere grid cell
    assert vermont_population.loc[1]["count"] == 2759


def test_plot_grid():
    pass


def test_export_grid():
    pass
