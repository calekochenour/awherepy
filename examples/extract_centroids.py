"""
Extract Centroids from aWhere Grid with aWherePy
================================================

Learn how to extract aWhere grid cell centroids using aWherePy.

"""

###############################################################################
# Extract Centroids from an aWhere Grid with aWherePy
# ---------------------------------------------------
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
# Extract Centroids from the aWhere Grid
# --------------------------------------
#
# Extract the centroids by calling the ``extract_centroids()`` function on a
# valid aWhere grid.

# Extract centroids
vt_grid_centroids = ag.extract_centroids(vt_grid)
