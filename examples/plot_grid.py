"""
Plot an aWhere Grid with aWherePy
=================================

Learn how to plot an aWhere grid with the shapefile used to create the grid
using aWherePy.

"""

###############################################################################
# Plot an aWhere grid with the Shapefile Used to Create the grid with aWherePy
# ----------------------------------------------------------------------------
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
# Import Packages
# ---------------
#
# In order to use the functionality in the``awherepy.grid`` module, the
# following packages need to be imported.

import os
import awherepy.grid as awg

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
vt_grid, vt_bound_4326 = awg.create_grid(vt_bound_path, buffer_distance=0.12)

###############################################################################
# Plot aWhere Grid and Shapefile Boundary
# ---------------------------------------
#
# Plot aWhere Grid and Shapefile Boundary by calling the ``plot_grid()``
# function on a valid aWhere grid (geopandas geodataframe with polygon
# geometry) and shapefile.

# Plot grid and boundary
fig, ax = awg.plot_grid(vt_grid, vt_bound_4326)

###############################################################################
# Plot aWhere Grid and Shapefile Boundary with Additional Parameters
# ------------------------------------------------------------------
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
