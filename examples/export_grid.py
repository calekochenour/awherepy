"""
Export an aWhere Grid with aWherePy
===================================

Learn how to export an aWhere grid to csv, shp, geojson, and gpkg formats
using aWherePy.

"""

###############################################################################
# Export an aWhere Grid to CSV, SHP, GEOJSON, and GPKG Formats with aWherePy
# ----------------------------------------------------------------------------
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
# Export aWhere Grid to CSV
# -------------------------
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
csv_export = ag.export_grid(vt_grid, csv_export_path)

###############################################################################
# Export aWhere Grid to SHP
# -------------------------
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
shp_export = ag.export_grid(vt_grid, shp_export_path)

###############################################################################
# Export aWhere Grid to GEOJSON
# -----------------------------
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
geojson_export = ag.export_grid(vt_grid, geojson_export_path)

###############################################################################
# Export aWhere Grid to GPKG
# --------------------------
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
gpkg_export = ag.export_grid(vt_grid, gpkg_export_path)
