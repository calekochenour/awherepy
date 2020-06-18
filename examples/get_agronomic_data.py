"""
Get Agronomic Data with aWherePy
================================

Learn how to get agronomic norms and observed values with aWherePy.

"""

###############################################################################
# Get Historical Norms and Observed Agronomic Data Data with aWherePy
# -------------------------------------------------------------------
#
# .. note::
#    The example below will show you how to use the ``get_agronomics_norms()``
#    and ``get_agronomic_values()`` functions to obtain agronomics data from
#    the aWhere agronomics API.
#
# In this vignette, you will use a single aWhere grid cell centroid near Rocky
# Mountain National Park, Colorado to get agronomic norms and observed values
# for May 4 - May 13. Agrnomic norms are data aggregated over many years and do
# not reference a specific year. The agronomic values for this example are from
# 2014. In addition, you will plot a comparison of the historical agronomic
# norms to the observed data in 2014.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import matplotlib.pyplot as plt
import awherepy.agronomics as awa
import awherepy.grid as awg

###############################################################################
# Prerequisites
# -------------
#
# In order to make calls to any aWhere API, you must provide a valid API key
# and secret. The key and secret used in this example are stored as
# environment variables.

# Define aWhere API key and secret
awhere_api_key = os.environ.get("AWHERE_API_KEY")
awhere_api_secret = os.environ.get("AWHERE_API_SECRET")

###############################################################################
# Extract Centroids from an aWhere Grid and Isolate a Centroid for Analysis
# -------------------------------------------------------------------------
#
# In order to use an aWhere grid cell centroid, you must first create an aWhere
# grid from a shapefile, extract all centroids, and isolate a single centroid.
# This functionality is found in the ``awherepy.grid module``.

# Define path to Rocky Mountain National Park, Colorado boundary
rmnp_bound_path = os.path.join(
    "..", "awherepy", "example-data", "colorado_rmnp_boundary.shp"
)

# Create aWhere grid and EPSG 4326 boudary for RMNP, CO
rmnp_grid, rmnp_bound_4326 = awg.create_grid(
    rmnp_bound_path, buffer_distance=0.12
)

# Plot RMNP grid and boundary - optional
fig, ax = awg.plot_grid(
    rmnp_grid,
    rmnp_bound_4326,
    plot_title="Rocky Mountain National Park, Colorado aWhere Grid",
    data_source="U.S. Department of the Interior",
)

# Extract RMNP grid centroids to list
rmnp_grid_centroids = awg.extract_centroids(rmnp_grid)

# Get first centroid
analysis_centroid = rmnp_grid_centroids[0]

###############################################################################
# Get aWhere Agronomic Norms Data
# -------------------------------
#
# Get aWhere agronomic norms data by calling the ``get_agronomic_norms()``
# function, with optional keyword arguments to use values outside the default.

# Define RMNP norms kwargs
rmnp_agronomic_norms_kwargs = {
    "location": (analysis_centroid[0], analysis_centroid[1]),
    "start_date": "05-04",
    "end_date": "05-13",
}

# Get RMNP agronomic norms, 05-04 to 05-13
rmnp_norms_total, rmnp_norms_daily = awa.get_agronomic_norms(
    awhere_api_key, awhere_api_secret, kwargs=rmnp_agronomic_norms_kwargs
)

# Get rolling total precipitation average
rmnp_precip_rolling_avg = rmnp_norms_daily[["precip_rolling_total_average_mm"]]

###############################################################################
# Get aWhere Agronomic Values Data
# --------------------------------
#
# Get aWhere observed agronomoc values data by calling the
# ``get_agronomic_values()`` function, with optional keyword arguments to use
# values outside the default.

# Define RMNP values kwargs
rmnp_agronomic_values_kwargs = {
    "location": (analysis_centroid[0], analysis_centroid[1]),
    "start_date": "2014-05-04",
    "end_date": "2014-05-13",
}

# Get observed agronomic values
rmnp_values_total, rmnp_values_daily = awa.get_agronomic_values(
    awhere_api_key, awhere_api_secret, kwargs=rmnp_agronomic_values_kwargs
)

# Get observed precipitation rolling total
rmnp_precip_rolling_observed = rmnp_values_daily[["precip_rolling_total_mm"]]

# Change date (YYYY-MM-DD) to day (MM-DD) for plotting
days = [value[5:] for value in rmnp_precip_rolling_observed.index.values]
rmnp_precip_rolling_observed.insert(1, "day", days, True)
rmnp_precip_rolling_observed.set_index("day", inplace=True)

###############################################################################
# Combine aWhere Agronomic Norms and Observed Values Data Subsets for Plotting
# ----------------------------------------------------------------------------
#
# Merge the agrnomic data subsets for precipitation into a single dataframe for
# use with plotting and visualiztion.

# Merge precipitation components (norms and observed values)
rmnp_precip_rolling_may_2014 = rmnp_precip_rolling_observed.merge(
    rmnp_precip_rolling_avg, on="day"
)

# Add column for difference between observed values and norms
rmnp_precip_rolling_may_2014["precip_rolling_diff_mm"] = (
    rmnp_precip_rolling_may_2014.precip_rolling_total_mm
    - rmnp_precip_rolling_may_2014.precip_rolling_total_average_mm
)

###############################################################################
# Plot a Comparison between the aWhere Norms and Observed Values for RMNP, CO
# ---------------------------------------------------------------------------
#
# Plot the norms and observed values on the same subplot and also the
# difference between the data on a second subplot to see which days in the May
# 4 - May 13 temporal extent showed higher or lower rolling total
# precipatation compared to the historic norms.

# Plot rolling total precip comparison
with plt.style.context("dark_background"):

    # Create figure and axes
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    # Set overall title
    plt.suptitle(
        (
            "Rocky Mountain National Park, CO\nLongitude: "
            f"{round(analysis_centroid[0], 4)}, Latitude: "
            f"{round(analysis_centroid[1], 4)}\nRolling Total Precipitation, "
            "May 2014"
        ),
        fontsize=24,
    )

    # Set spacing
    plt.subplots_adjust(top=0.8)

    # Subplot 1 - Observed and Historic Rolling Precipitation
    # Add grid
    ax[0].grid(zorder=1)

    # Add daily observed rolling total (line)
    ax[0].plot(
        rmnp_precip_rolling_may_2014.precip_rolling_total_mm,
        marker="o",
        color="#7fc97f",
        markersize=8,
        linewidth=2,
        linestyle="--",
        zorder=2,
    )

    # Add observed rolling total (fill)
    ax[0].fill_between(
        rmnp_precip_rolling_may_2014.index.values,
        rmnp_precip_rolling_may_2014.precip_rolling_total_mm,
        label="Observed Rolling Total",
        color="#7fc97f",
        linewidth=0.5,
        linestyle="-",
        zorder=2,
        alpha=1,
    )

    # Add daily average rolling total (line)
    ax[0].plot(
        rmnp_precip_rolling_may_2014.precip_rolling_total_average_mm,
        marker="o",
        color="#beaed4",
        markersize=8,
        linewidth=2,
        linestyle="--",
        zorder=3,
    )

    # Add average rolling total (fill)
    ax[0].fill_between(
        rmnp_precip_rolling_may_2014.index.values,
        rmnp_precip_rolling_may_2014.precip_rolling_total_average_mm,
        label="Average Rolling Total",
        color="#beaed4",
        linewidth=2,
        linestyle="-",
        zorder=2,
        alpha=1,
    )

    # Configure axes
    ax[0].set_xlabel("Date", fontsize=16)
    ax[0].set_ylabel("Precipitation (mm)", fontsize=16)
    ax[0].set_title("Rolling Total Precipitation", fontsize=20)
    ax[0].tick_params(axis="both", which="major", labelsize=16)
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45)

    # Add legend
    ax[0].legend(borderpad=0.75, edgecolor="w", fontsize=16, shadow=True)

    # Subplot 2 - Rolling Precipitation Difference
    # Add grid
    ax[1].grid(zorder=1)

    # Add difference (observed - norms)
    ax[1].bar(
        rmnp_precip_rolling_may_2014.index.values,
        rmnp_precip_rolling_may_2014.precip_rolling_diff_mm,
        label="Rolling Total Difference",
        zorder=2,
        edgecolor="#ff7f00",
        color="#fdc086",
        linewidth=1,
    )

    # Configure axes
    ax[1].set_xlabel("Date", fontsize=16)
    ax[1].set_ylabel("Precipitation Difference (mm)", fontsize=16)
    ax[1].set_title(
        "Precipitation Difference (Observed - Average)", fontsize=20
    )
    ax[1].tick_params(axis="both", which="major", labelsize=16)
    plt.setp(ax[1].xaxis.get_majorticklabels(), rotation=45)

    # Add legend
    ax[1].legend(borderpad=0.75, edgecolor="w", fontsize=16, shadow=True)

    plt.show()
