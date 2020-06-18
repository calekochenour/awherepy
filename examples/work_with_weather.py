"""
Work with Weather Data in aWherePy
==================================

Learn how to get weather norms and observed weather with aWherePy.

"""

###############################################################################
# Get Historical Norms and Observed Weather Data with aWherePy
# ------------------------------------------------------------
#
# .. note::
#    The example below will show you how to use the ``get_weather_norms()`` and
#    ``get_weather_observed()`` functions to obtain weather data from the
#    aWhere weather API.
#
# In this vignette, you will use a single aWhere grid cell centroid near Rocky
# Mountain National Park, Colorado to get weather norms and observed weather
# for May 4 - May 13. Weather norms are data aggregated over many years and do
# not reference a specific year. The observed weather for this example is from
# 2014. In addition, you will plot a comparison of the historical weather norms
# to the observed data in 2014.

###############################################################################
# Import Packages
# ---------------
#
# In order to use the functionality in this example, the following packages
# need to be imported.

import os
import matplotlib.pyplot as plt
import awherepy.grid as awg
import awherepy.weather as aww

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
# Get aWhere Weather Norms Data
# -----------------------------
#
# Get aWhere weather norms data by calling the ``get_weather_norms()``
# function, with optional keyword arguments to use values outside the default.

# Define RMNP norms kwargs
rmnp_weather_norms_kwargs = {
    "location": (analysis_centroid[0], analysis_centroid[1]),
    "start_date": "05-04",
    "end_date": "05-13",
}

# Get RMNP weather norms, 05-04 to 05-13
rmnp_weather_norms = aww.get_weather_norms(
    awhere_api_key, awhere_api_secret, kwargs=rmnp_weather_norms_kwargs
)

# Get precipitation average from weather norms data
rmnp_precip_norms = rmnp_weather_norms[["precip_avg_mm"]]

###############################################################################
# Get aWhere Weather Observed Data
# --------------------------------
#
# Get aWhere weather observed data by calling the ``get_weather_observed()``
# function, with optional keyword arguments to use values outside the default.

# Define RMNP observed kwargs
rmnp_weather_observed_kwargs = {
    "location": (analysis_centroid[0], analysis_centroid[1]),
    "start_date": "2014-05-04",
    "end_date": "2014-05-13",
}

# Get observed weather
rmnp_weather_observed = aww.get_weather_observed(
    awhere_api_key, awhere_api_secret, kwargs=rmnp_weather_observed_kwargs
)

# Get precipitation amount from observed weather
rmnp_precip_observed = rmnp_weather_observed[["precip_amount_mm"]]

# Change date (YYYY-MM-DD) to day (MM-DD) for plotting
days = [value[5:] for value in rmnp_precip_observed.index.values]
rmnp_precip_observed.insert(1, "day", days, True)
rmnp_precip_observed.set_index("day", inplace=True)

###############################################################################
# Combine aWhere Weather Norms and Observed Data Subsets for Plotting
# -------------------------------------------------------------------
#
# Merge the weather data subsets for precipitation into a single dataframe for
# use with plotting and visualiztion.

# Merge precipitation components (norms and observed)
rmnp_precip_may_2014 = rmnp_precip_observed.merge(rmnp_precip_norms, on="day")

# Add column for difference between observed and norms
rmnp_precip_may_2014["precip_diff_mm"] = (
    rmnp_precip_may_2014.precip_amount_mm - rmnp_precip_may_2014.precip_avg_mm
)

###############################################################################
# Plot a Comparison between the aWhere Norms and Observed Data for RMNP, CO
# -------------------------------------------------------------------------
#
# Plot the norms and observed data on the same subplot and also the difference
# between the data on a second subplot to see which days in the May 4 - May 13
# temporal extent showed higher or lower precipatation compared to the historic
# norms.

# Plot daily precip comparison
with plt.style.context("dark_background"):

    # Create figure and axes
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

    # Set overall title
    plt.suptitle(
        (
            "Rocky Mountain National Park, CO\nLongitude: "
            f"{round(analysis_centroid[0], 4)}, Latitude: "
            f"{round(analysis_centroid[1], 4)}\nPrecipitation, May 2014"
        ),
        fontsize=24,
    )

    # Set spacing
    plt.subplots_adjust(top=0.8)

    # Subplot 1 - Observed and Historic Precipitation
    # Add grid
    ax[0].grid(zorder=1)

    # Add daily observed total (line)
    ax[0].plot(
        rmnp_precip_may_2014.precip_amount_mm,
        label="Observed",
        marker="o",
        color="#7fc97f",
        markersize=8,
        linewidth=2,
        linestyle="--",
        zorder=2,
    )

    # Add daily average total (line)
    ax[0].plot(
        rmnp_precip_may_2014.precip_avg_mm,
        label="Historic Average",
        marker="o",
        color="#beaed4",
        markersize=8,
        linewidth=2,
        linestyle="--",
        zorder=3,
    )

    # Configure axes
    ax[0].set_xlabel("Date", fontsize=16)
    ax[0].set_ylabel("Precipitation (mm)", fontsize=16)
    ax[0].set_title("Daily Total Precipitation", fontsize=20)
    ax[0].tick_params(axis="both", which="major", labelsize=16)
    plt.setp(ax[0].xaxis.get_majorticklabels(), rotation=45)

    # Add legend
    ax[0].legend(borderpad=0.75, edgecolor="w", fontsize=16, shadow=True)

    # Subplot 2 - Precipitation Difference
    # Add grid
    ax[1].grid(zorder=1)

    # Add difference (observed - norms)
    ax[1].bar(
        rmnp_precip_may_2014.index.values,
        rmnp_precip_may_2014.precip_diff_mm,
        label="Daily Total Difference",
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
