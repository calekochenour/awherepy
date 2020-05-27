"""
Rasterize Data to the aWhere Grid with aWherePy
===============================================

Learn how to resample existing raster data to the aWhere grid cell using
aWherePy.

"""

###############################################################################
# Resample Rasterized Data to the aWhere Grid with aWherePy
# ---------------------------------------------------------
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
# Import Packages
# ---------------
#
# In order to use the functionality in the``awherepy.grid`` module, the
# following packages need to be imported.

import os
import awherepy.grid as ag

###############################################################################
# Prerequisites
# -------------
#
# In order to extract centroids, you must first create aWhere grid from a
# shapefile.

# Define path to Vermont boundary shapefile
vt_bound_path = os.path.join(
    "..", "awherepy", "example-data", "vermont_state_boundary.shp"
)

# Create aWhere grid and EPSG 4326 boundary from Vermont shapefile
vt_grid, vt_bound_4326 = ag.create_grid(vt_bound_path, buffer_distance=0.12)

###############################################################################
# Set Path to World Population Data (2020) for Vermont State
# ----------------------------------------------------------
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
# ----------------------------------------------------
#
# The ``rasterize()`` function uses zonal statistics to re-sample finer
# spatial resolution data to the aWhere grid size of 9x9 km. By default, the
# ``rasterize()`` function adds the count of cells used the calulation and
# the raw sum of data for all cells within each aWhere grid cell. Add the
# resamples data to the aWhere grid by callin the ``rasterize()`` function
# on a valid aWhere grid (geopandas geodataframe with polygon geometry) and
# and a georeferenced raster with finer spatial resolution.

# Rasterize Vermont population data (100x100 m) to aWhere grid (9x9 km)
vt_pop_2020_rasterized = ag.rasterize(vt_grid, vt_pop_2020_path)

###############################################################################
# Rasterize Data to the aWhere Grid with Additional Zonal Statistics
# ------------------------------------------------------------------
#
# The ``rasterize()`` by default only includes the count and sum statistics.
# Additional statistics can be computed by added to the ``zonal_stats``
# parameter within the ``rasterize()`` function. Valid statistics include all
# items in the ``rasterstats.utils.VALID_STATS`` list. Additional information
# can be found by calling help on the ``rasterstats.gen_zonal_stats()``
# function.

# Rasterize Vermont population data with additional summary statistics
vt_pop_2020_rasterized = ag.rasterize(
    vt_grid, vt_pop_2020_path, statistics="count sum min max mean median"
)
