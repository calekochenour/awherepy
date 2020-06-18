"""Tests for the grids module."""

import os
import pytest
import matplotlib as mpl
import shapely
import geopandas as gpd
import awherepy.grids as awg


@pytest.fixture
def vermont_grid():
    """Fixture that returns the aWhere grid for
    the state of Vermont.
    """
    # Define path to shapefile boundary
    vt_bound_path = os.path.join(
        "awherepy", "example-data", "vermont_state_boundary.shp"
    )

    # Create aWhere grid and boundary
    vt_grid, vt_bound_4326 = awg.create_grid(
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
    vt_bound_path = os.path.join(
        "awherepy", "example-data", "vermont_state_boundary.shp"
    )

    # Create aWhere grid and boundary
    vt_grid, vt_bound_4326 = awg.create_grid(
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
    vt_centroids = awg.extract_centroids(vermont_grid)

    # Return centroids
    return vt_centroids


@pytest.fixture
def vermont_population(vermont_grid):
    """Fixture that returns 100x100 meter population
    grid rasterized to the Vermont aWhere grid (9x9 km).
    """
    # Define path to Vermont 2020 population per pixel
    vt_pop_path = os.path.join("awherepy", "example-data", "vt_ppp_2020.tif")

    # Rasterize ppp data (100x100 m) to aWhere grid (9x9 km)
    vt_pop_rasterized = awg.rasterize(vermont_grid, vt_pop_path)

    # Return geodataframe with rasterized pop data
    return vt_pop_rasterized


@pytest.fixture
def vermont_plot_figure(vermont_grid, vermont_boundary):
    """Fixture that returns a plot figure for the
    Vermont aWhere grid and boudary plotted on the same
    axes.
    """
    # Plot grid and boundary
    fig, ax = awg.plot_grid(vermont_grid, vermont_boundary)

    # Return figure
    return fig


@pytest.fixture
def vermont_plot_axes(vermont_grid, vermont_boundary):
    """Fixture that returns a plot axes for the
    Vermont aWhere grid and boudary plotted on the same
    axes.
    """
    # Plot grid and boundary
    fig, ax = awg.plot_grid(vermont_grid, vermont_boundary)

    # Return axes
    return ax


@pytest.fixture
def vermont_grid_csv(vermont_grid):
    """Fixture that returns the path to an exported
    CSV for the Vermont aWhere grid.
    """
    # Define output path
    outpath = os.path.join("awherepy", "example-data", "vermont_grid.csv")

    # Remove file if already exists
    if os.path.exists(outpath):
        os.remove(outpath)

    # Export file
    export = awg.export_grid(vermont_grid, outpath)

    # Return exported file path
    return export


@pytest.fixture
def vermont_grid_shp(vermont_grid):
    """Fixture that returns the path to an exported
    SHP for the Vermont aWhere grid.
    """
    # Define output path
    outpath = os.path.join("awherepy", "example-data", "vermont_grid.shp")

    # Remove file if already exists
    if os.path.exists(outpath):
        os.remove(outpath)

    # Export file
    export = awg.export_grid(vermont_grid, outpath)

    # Return exported file path
    return export


@pytest.fixture
def vermont_grid_geojson(vermont_grid):
    """Fixture that returns the path to an exported
    GEOJSON for the Vermont aWhere grid.
    """
    # Define output path
    outpath = os.path.join("awherepy", "example-data", "vermont_grid.geojson")

    # Remove file if already exists
    if os.path.exists(outpath):
        os.remove(outpath)

    # Export file
    export = awg.export_grid(vermont_grid, outpath)

    # Return exported file path
    return export


@pytest.fixture
def vermont_grid_gpkg(vermont_grid):
    """Fixture that returns the path to an exported
    GPKG for the Vermont aWhere grid.
    """
    # Define output path
    outpath = os.path.join("awherepy", "example-data", "vermont_grid.gpkg")

    # Remove file if already exists
    if os.path.exists(outpath):
        os.remove(outpath)

    # Export file
    export = awg.export_grid(vermont_grid, outpath)

    # Return exported file path
    return export


@pytest.fixture
def vermont_grid_gpx(vermont_grid):
    """Fixture that returns the path to an exported
    GPX for the Vermont aWhere grid. Designed to fail.
    Unsupported export file type.
    """
    # Define output path
    outpath = os.path.join("awherepy", "example-data", "vermont_grid.gpx")

    # Remove file if already exists
    if os.path.exists(outpath):
        os.remove(outpath)

    # Export file
    export = awg.export_grid(vermont_grid, outpath)

    # Return exported file path
    return export


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

    # First centroid; round to 4 digits
    lon_first_round = round(vermont_centroids[0][0], 4)
    lat_first_round = round(vermont_centroids[0][1], 4)
    assert (lon_first_round, lat_first_round) == (-73.4378, 43.5270)

    # Last centroid; round to 4 digits
    lon_last_round = round(vermont_centroids[-1][0], 4)
    lat_last_round = round(vermont_centroids[-1][1], 4)
    assert (lon_last_round, lat_last_round) == (-71.4378, 45.0470)


def test_rasterize(vermont_population):
    """Test aWhere-rasterized ppp data for Vermont.
    """
    # Grid should be a geopandas geodataframe
    assert isinstance(vermont_population, gpd.geodataframe.GeoDataFrame)

    # Population sum column should be in geodataframe
    assert "sum" in vermont_population.columns

    # Number of 100x100 m cells rasterized to aWhere grid cell
    assert vermont_population.loc[1]["count"] == 2759


def test_plot_grid(vermont_plot_figure, vermont_plot_axes):
    """The the plot of the aWhere grid and study
    area boundary for Vermont.
    """
    # Test figure type
    assert isinstance(vermont_plot_figure, mpl.figure.Figure)

    # Test figure width
    assert vermont_plot_figure.get_figwidth() == 20.0

    # Test figure height
    assert vermont_plot_figure.get_figheight() == 10.0

    # Test axes type
    assert isinstance(vermont_plot_axes, mpl.axes._subplots.Axes)

    # Test axes subplot geometry
    assert vermont_plot_axes.get_geometry() == (1, 1, 1)

    # Test axes column start location
    assert vermont_plot_axes.get_subplotspec().colspan.start == 0

    # Test axes row start location
    assert vermont_plot_axes.get_subplotspec().rowspan.start == 0

    # Test only one axis in axes object
    with pytest.raises(TypeError):
        vermont_plot_axes[0]


def test_export_grid(
    vermont_grid_csv,
    vermont_grid_shp,
    vermont_grid_geojson,
    vermont_grid_gpkg,
    vermont_grid,
):
    """Test grid export to CSV, SHP, GEOJSON, and GPKG
    for the Vermont aWhere grid.
    """
    # Test existence of csv
    assert os.path.exists(vermont_grid_csv)

    # Test csv file extension
    assert vermont_grid_csv.split(".")[-1] == "csv"

    # Test existence of csv
    assert os.path.exists(vermont_grid_shp)

    # Test shp file extension
    assert vermont_grid_shp.split(".")[-1] == "shp"

    # Test existence of geojson
    assert os.path.exists(vermont_grid_geojson)

    # Test geojson file extension
    assert vermont_grid_geojson.split(".")[-1] == "geojson"

    # Test existence of gpkg
    assert os.path.exists(vermont_grid_gpkg)

    # Test gpkg file extension
    assert vermont_grid_gpkg.split(".")[-1] == "gpkg"

    # Test invalid export file type (GPX)
    with pytest.raises(OSError):
        awg.export_grid(
            vermont_grid, os.path.join("test-data", "vermont_grid.gpx")
        )
