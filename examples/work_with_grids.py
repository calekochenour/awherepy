"""
Work with Grids in aWherePy
===========================

Learn how to create grids, plot grids, export grids, extract grid centroids,
and rasterize data to grids with aWherePy.

"""

###############################################################################
# Prerequisites
# -------------
#
# In order to run the examples, you must complete the following prerequisites.

###############################################################################
# Import Packages
# ~~~~~~~~~~~~~~~
#
# In order to use the functionality in the ``awherepy.grids`` module, the
# following packages need to be imported.

import os
import awherepy.grids as awg

###############################################################################
# Set Path to Study Area Boundary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the Vermont state boundary shapefile. The
# path is valid if the script is run from the 'examples' directory. Otherwise,
# you will have to specify a different path to the shapefile, relative to
# your local computer.

# Define path to Vermont boundary shapefile
vt_bound_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_state_boundary.shp"
)

###############################################################################
# Create an aWhere Grid with aWherePy
# -----------------------------------
#
# Learn how to create an aWhere-sized (9x9 km) grid from a shapefile
# using aWherePy.

###############################################################################
# Create aWhere-Sized Grid from a Shapefile with aWherePy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. note::
#    The example below will show you how to use the ``create_grid()``
#    function to create a grid of 9x9 km (0.08 x 0.08 degrees, 5x5
#    arc-minutes) cells from a shapefile using Python.
#
# In this vignette, you will use a shapefile for the Vermont state boundary
# to create an aWhere-sized grid. The ``create_grid()`` function returns the
# aWhere grid and the input shapefile projected to EPSG 4326, which is useful
# for plotting with the aWhere grid (also projected to EPSG 4326).


###############################################################################
# Define Buffer Distance and Create Grid
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Create the aWhere-grid by specifying the buffer distance (in degrees) for
# grid, to ensure the entire study area is covered within the grid. The buffer
# distance is the distance that the shapefile will be buffered by prior to
# the creation of the aWhere grid. The ``create_grid()`` function creates
# the grid from the buffered version of the shapefile.

# Define buffer distance (degrees)
vt_buffer_deg = 0.12

# Create aWhere grid and EPSG 4326 boundary from Vermont shapefile
vt_grid, vt_bound_4326 = awg.create_grid(
    vt_bound_path, buffer_distance=vt_buffer_deg
)

###############################################################################
# Use a Different Buffer Distance to Create the aWhere Grid
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Some study areas, depending on size, may require a different buffer Distance
# to create a grid that captures the full study area. This can be accomplished
# by changing the ``buffer_distance`` parameter in the ``create_grid()``
# function to a different number.

# Define new buffer distance (degrees)
vt_buffer_new_deg = 0.25

# Create aWhere grid and EPSG 4326 boundary from Vermont shapefile with the
# new buffer distance
vt_grid_new, vt_bound_4326 = awg.create_grid(
    vt_bound_path, buffer_distance=vt_buffer_new_deg
)

###############################################################################
# Plot an aWhere Grid with aWherePy
# ---------------------------------
#
# Learn how to plot an aWhere grid with the shapefile used to create the grid
# using aWherePy.

###############################################################################
# Plot an aWhere grid with the Shapefile Used to Create the grid with aWherePy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. note::
#    The example below will show you how to use the ``plot_grid()`` to plot
#    an aWhere grid and the shapefile used to create the grid on the same plot
#    axes.
#
# In this vignette, you will use an aWhere grid and shapefile for the Vermont
# state boundary to plot both on the same axes. The plot will provide a visual
# that can aid in determining if you should change the buffer size for the
# aWhere grid, in cases where there are too many grid cells (some do not
# overlap the shapefile) or in cases where there are too few grid cells (the
# shapefile extends outside the grid).

###############################################################################
# Plot aWhere Grid and Shapefile Boundary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Plot aWhere Grid and Shapefile Boundary by calling the ``plot_grid()``
# function on a valid aWhere grid (geopandas geodataframe with polygon
# geometry) and shapefile.

# Plot grid and boundary
fig, ax = awg.plot_grid(vt_grid, vt_bound_4326)

###############################################################################
# Plot aWhere Grid and Shapefile Boundary with Additional Parameters
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# By default, the ``plot_grid()`` adds a title of 'aWhere Grid' and does not
# include a data source. This information can be added by specifying the
# ``plot_title`` and ``data_source`` parameters during the call to the
# ``plot_grid()`` function.

# Plot grid and boundary with custom title and data source
fig, ax = awg.plot_grid(
    vt_grid,
    vt_bound_4326,
    plot_title="Vermont State aWhere Grid",
    data_source="State of Vermont",
)

###############################################################################
# Export an aWhere Grid with aWherePy
# -----------------------------------
#
# Learn how to export an aWhere grid to csv, shp, geojson, and gpkg formats
# using aWherePy.

###############################################################################
# Export an aWhere Grid to CSV, SHP, GEOJSON, and GPKG Formats with aWherePy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. note::
#    The example below will show you how to use the ``export_grid()`` function
#    to export the aWhere grid (geopandas geodataframe) to the following file
#    formats:
#
#      - Comma-separate value (.csv);
#      - Shapefile (.shp);
#      - GeoJSON (.geojson); and,
#      - Geopackage (.gpkg).
#
# In this vignette, you will export the Vermont state aWhere grid to csv, shp,
# geojson, and gpkg formats.

###############################################################################
# Export aWhere Grid to CSV
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the output Vermont aWhere grid CSV. The
# path is valid if the script is run from the 'examples' directory. Otherwise,
# you will have to specify a different path to the shapefile, relative to
# your local computer. # Export the aWhere grid by calling the
# ``export_grid()`` function on a valid aWhere grid and valid output path.

# Define path to output Vermont aWhere grid csv
csv_export_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_grid.csv"
)

# Export grid to CSV
csv_export = awg.export_grid(vt_grid, csv_export_path)

###############################################################################
# Export aWhere Grid to SHP
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the output Vermont aWhere grid SHP. The
# path is valid if the script is run from the 'examples' directory. Otherwise,
# you will have to specify a different path to the shapefile, relative to
# your local computer. # Export the aWhere grid by calling the
# ``export_grid()`` function on a valid aWhere grid and valid output path.

# Define path to output Vermont aWhere grid shp
shp_export_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_grid.shp"
)

# Export grid to SHP
shp_export = awg.export_grid(vt_grid, shp_export_path)

###############################################################################
# Export aWhere Grid to GEOJSON
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the output Vermont aWhere grid GEOJSON. The
# path is valid if the script is run from the 'examples' directory. Otherwise,
# you will have to specify a different path to the shapefile, relative to
# your local computer. Export the aWhere grid by calling the ``export_grid()``
# function on a valid aWhere grid and valid output path.

# Define path to output Vermont aWhere grid geojson
geojson_export_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_grid.geojson"
)

# Export grid to GEOJSON
geojson_export = awg.export_grid(vt_grid, geojson_export_path)

###############################################################################
# Export aWhere Grid to GPKG
# ~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the output Vermont aWhere grid GPKG. The
# path is valid if the script is run from the 'examples' directory. Otherwise,
# you will have to specify a different path to the shapefile, relative to
# your local computer. Export the aWhere grid by calling the ``export_grid()``
# function on a valid aWhere grid and valid output path.

# Define path to output Vermont aWhere grid gpkg
gpkg_export_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_grid.gpkg"
)

# Export grid to GPKG
gpkg_export = awg.export_grid(vt_grid, gpkg_export_path)

###############################################################################
# Extract Centroids from an aWhere Grid with aWherePy
# ---------------------------------------------------
#
# Learn how to extract aWhere grid cell centroids using aWherePy.

###############################################################################
# Extract Centroids from an aWhere Grid with aWherePy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. note::
#    The example below will show you how to use the ``extract_centroids()``
#    function to extract the cell centroids from an aWhere grid using Python.
#
# In this vignette, you will use an aWhere grid for the Vermont state boundary
# to extract grid cell centroids. The ``extract_centroids()`` function returns
# a list of (longitude, latitude) centroids for all grid cells. The coordinates
# of the centroids are in EPSG 4326.

###############################################################################
# Extract Centroids from the aWhere Grid
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Extract the centroids by calling the ``extract_centroids()`` function on a
# valid aWhere grid.

# Extract centroids
vt_grid_centroids = awg.extract_centroids(vt_grid)

###############################################################################
# Rasterize Data to the aWhere Grid with aWherePy
# -----------------------------------------------
# Learn how to resample existing raster data to the aWhere grid cell using
# aWherePy.

###############################################################################
# Resample Rasterized Data to the aWhere Grid with aWherePy
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# .. note::
#    The example below will show you how to use the ``rasterize()`` function
#    to resample raster data to the tile size of the aWhere grid.
#
# In this vignette, you will use an aWhere grid for the Vermont state boundary
# to resample world population data for the state of Vermont from 100x100 meter
# spatial resoltion to the 9x9 km spatial resolution of the aWhere grid.
# Population from this data set is defined as population per pixel (ppp).

###############################################################################
# Set Path to World Population Data (2020) for Vermont State
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# To get started, set the path to the Vermont state world population GeoTiff
# file. The path is valid if the script is run from the 'examples' directory.
# Otherwise, you will have to specify a different path to the shapefile,
# relative to your local computer.

# Define path to Vermont population data
vt_pop_2020_path = os.path.join(
    "..", "awherepy", "example-data", "vt_ppp_2020.tif"
)

###############################################################################
# Rasterize Vermont Population Data to the aWhere Grid
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The ``rasterize()`` function uses zonal statistics to re-sample finer
# spatial resolution data to the aWhere grid size of 9x9 km. By default, the
# ``rasterize()`` function adds the count of cells used the calulation and
# the raw sum of data for all cells within each aWhere grid cell. Add the
# resamples data to the aWhere grid by callin the ``rasterize()`` function
# on a valid aWhere grid (geopandas geodataframe with polygon geometry) and
# and a georeferenced raster with finer spatial resolution.

# Rasterize Vermont population data (100x100 m) to aWhere grid (9x9 km)
vt_pop_2020_rasterized = awg.rasterize(vt_grid, vt_pop_2020_path)

###############################################################################
# Rasterize Data to the aWhere Grid with Additional Zonal Statistics
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The ``rasterize()`` by default only includes the count and sum statistics.
# Additional statistics can be computed by added to the ``zonal_stats``
# parameter within the ``rasterize()`` function. Valid statistics include all
# items in the ``rasterstats.utils.VALID_STATS`` list. Additional information
# can be found by calling help on the ``rasterstats.gen_zonal_stats()``
# function.

# Rasterize Vermont population data with additional summary statistics
vt_pop_2020_rasterized = awg.rasterize(
    vt_grid, vt_pop_2020_path, statistics="count sum min max mean median"
)
