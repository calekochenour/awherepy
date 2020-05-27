"""
Create an aWhere Grid with aWherePy
===================================

Learn how to create an aWhere-sized (9x9 km) grid from a shapefile
using aWherePy.

"""

###############################################################################
# Create aWhere-Sized Grid from a Shapefile with aWherePy
# -------------------------------------------------------
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
# Import Packages
# ---------------
#
# In order to use the functionality in the``awherepy.grid`` module, the
# following packages need to be imported.

import os
import awherepy.grid as ag

###############################################################################
# Set Path to Study Area Boundary
# -------------------------------
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
# Define Buffer Distance and Create Grid
# ---------------------------------------
#
# Create the aWhere-grid by specifying the buffer distance (in degrees) for
# grid, to ensure the entire study area is covered within the grid. The buffer
# distance is the distance that the shapefile will be buffered by prior to
# the creation of the aWhere grid. The ``create_grid()`` function creates
# the grid from the buffered version of the shapefile.

# Define buffer distance (degrees)
vt_buffer_deg = 0.12

# Create aWhere grid and EPSG 4326 boundary from Vermont shapefile
vt_grid, vt_bound_4326 = ag.create_grid(
    vt_bound_path, buffer_distance=vt_buffer_deg
)

###############################################################################
# Use a Different Buffer Distance to Create the aWhere Grid
# ---------------------------------------------------------
#
# Some study areas, depending on size, may require a different buffer Distance
# to create a grid that captures the full study area. This can be accomplished
# by changing the ``buffer_distance`` parameter in the ``create_grid()``
# function to a different number.

# Define new buffer distance (degrees)
vt_buffer_new_deg = 0.25

# Create aWhere grid and EPSG 4326 boundary from Vermont shapefile with the
# new buffer distance
vt_grid_new, vt_bound_4326 = ag.create_grid(
    vt_bound_path, buffer_distance=vt_buffer_new_deg
)
