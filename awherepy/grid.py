"""
awherepy.grid
=============
A module to create and work with aWhere grids.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
from shapely.geometry import Polygon
import geopandas as gpd
import rasterstats as rs


def create_grid(study_area_path, buffer_distance, cell_size=0.08):
    """Creates an aWhere-sized grid (0.08 x 0.08 degree,
    5 arc-minute x 5 arc-minute grid) fit to a polygon.

    Parameters
    ----------
    study_area_path : str
        Path the polygon shapefile boundary.

    buffer_distance : int or float
        Buffer size in degrees (WGS 84 CRS).

    cell_size: int or float
        Grid size (x and y dimension) in degrees (WGS 84 CRS).

    Returns
    -------
    study_area_grid_4326: geopandas GeoDataFrame
        Grid dataframe shaped to the polygon boundary.

    study_area_4326: geopandas GeoDataFrame
        Study area boundary projected to WGS 84, EPSG 4326.

    Example
    -------
        >>> # Import packages
        >>> import os
        >>> import geopandas as gpd
        >>> # Define path to shapefile boundary
        >>> vt_bound_path = os.path.join(
        ...     working_directory, 'shapefiles', 'vermont_state_boundary.shp')
        >>> # Create aWhere grid
        >>> vt_grid, vt_bound_4326 = create_grid(
        ...     vt_bound_path, buffer_distance=0.12)
        >>> # Plot aWhere grid
        >>> vt_grid.plot(facecolor="none", edgecolor="#984ea3", linewidth=1.5)
    """
    # Read shapefile into geodataframe
    study_area = gpd.read_file(study_area_path)

    # Project to WGS 84 Lat/Lon, EPSG 4326 if no CRS match
    if not study_area.crs == "epsg:4326":
        study_area_4326 = study_area.to_crs("epsg:4326")

    else:
        study_area_4326 = study_area

    # Create buffer around state boundary
    study_area_4326_buffer = study_area_4326.buffer(distance=buffer_distance)

    # Convert buffer from geoseries to geodataframe
    study_area_4326_buffer_gdf = gpd.GeoDataFrame(
        study_area_4326_buffer, crs="epsg:4326"
    )

    # Rename geometry column in buffer
    study_area_4326_buffer_gdf.rename(columns={0: "geometry"}, inplace=True)

    # Get extent of buffered boundary
    longitude_min = study_area_4326_buffer_gdf.bounds.minx[0]
    latitude_min = study_area_4326_buffer_gdf.bounds.miny[0]
    longitude_max = study_area_4326_buffer_gdf.bounds.maxx[0]
    latitude_max = study_area_4326_buffer_gdf.bounds.maxy[0]

    # Create lists for lat/lon extents
    longitude_vals = np.arange(longitude_min, longitude_max, cell_size)
    latitude_vals = np.arange(latitude_min, latitude_max, cell_size)

    # Create grid of polygons based on longitude and latitude ranges
    grid_polys_list = [
        Polygon(
            [
                (longitude, latitude),
                (longitude + cell_size, latitude),
                (longitude + cell_size, latitude + cell_size),
                (longitude, latitude + cell_size),
            ]
        )
        for longitude in longitude_vals
        for latitude in latitude_vals
    ]

    # Create geodataframe from grid polygons
    grid_polys_gdf = gpd.GeoDataFrame(crs=4326, geometry=grid_polys_list)

    # Narrow grid cells to those within the buffered boundary
    study_area_grid_4326 = gpd.sjoin(
        grid_polys_gdf, study_area_4326_buffer_gdf, op="within"
    )

    # Drop unnecessary colum
    study_area_grid_4326.drop(columns="index_right", inplace=True)

    # Return gridded geodataframe
    return study_area_grid_4326, study_area_4326


def extract_centroids(grid):
    """Extracts the longitude and latitude centroids
    from a grid of polygons.

    Parameters
    ----------
    grid : geopandas GeoDataFrame
        Grid dataframe with polygon geometry.

    Returns
    -------
    centroid_list: list (of tuples)
        List containing (longitude, latitude) tuples.

    Example
    -------
        >>> # Extract centroids
        >>> vt_grid_centroids = extract_centroids(vt_grid)
        >>> # Show number of centroids/grid cells
        >>> len(vt_grid_centroids)
        533
        >>> # Show first centroid
        >>> vt_grid_centroids[0]
        (-73.43784136769847, 43.527012318617274)
    """
    # Create copy of dataframe (avoids altering the original)
    grid_extract = grid.copy()

    # Add centroid to each grid cell
    grid_extract["centroid"] = grid_extract.geometry.apply(
        lambda poly: poly.centroid
    )

    # Extract latitude and longitude to new columns
    grid_extract["longitude"] = grid_extract.centroid.apply(
        lambda point: point.x
    )

    grid_extract["latitude"] = grid_extract.centroid.apply(
        lambda point: point.y
    )

    # Extract centroid (as tuples) from grid
    centroid_list = [
        (row.longitude, row.latitude) for row in grid_extract.itertuples()
    ]

    # Return centroids
    return centroid_list


def rasterize(awhere_grid, raster_path, zonal_stats="count sum"):
    """Rasterizes values from a GeoTiff (or other
    georeferenced raster) to the aWhere grid (9x9 km).

    Aggregates the sum by default.

    Parameters
    ----------
    awhere_grid : geopandas geodataframe
        Geodataframe containing a grid of aWhere-sized
        cells, sized to fit a shapefile boundary.

    raster_path : str
        Path to the data the will be rasterized.

    zonal_stats : space-delimited str (optional)
        Zonal statistics to calculate. Default value
        is 'count sum'.

    Returns
    -------
    awhere_grid_rasterized : geopandas geodataframe
        Input geodataframe with the rasterized values
        and grid centroids added.

    Example
    -------
        >>> # Import packages
        >>> import os
        >>> import geopandas as gpd
        >>> # Define path to shapefile boundary
        >>> vt_bound_path = os.path.join(
        ...     working_directory, 'shapefiles',
        ...     vermont_state_boundary.shp')
        >>> # Create aWhere grid for Vermont
        >>> vt_grid, vt_bound_4326 = create_grid(
        ...     vt_bound_path, buffer_distance=0.12)
        >>> # Define path to Vermont 2020 population per pixel
        >>> vt_pop_path = os.path.join(
        ...     working_directory, 'geotiffs',
        ...     'vt_ppp_2020.tif')
        >>> # Rasterize pop data (100x100 m) to aWhere grid (9x9 km)
        >>> vt_pop_rasterized = rasterize(vt_grid, vt_pop_path)
        >>> # Display single entry in resulting geodataframe
        >>> vt_pop_rasterized.loc[1]
        geometry    POLYGON ((-73.4778398510704 43.56701241643375,...
        centroid         POINT (-73.43783985107041 43.60701241643375)
        count                                                    2759
        sum                                                   12.7015
        Name: 1, dtype: object
    """
    # Open data for rasterizing
    with rio.open(raster_path) as src:

        # Extract array and metadata
        src_arr = src.read(1, masked=True)
        src_meta = src.profile

    # Create copy of input geodataframe
    awhere_grid_copy = awhere_grid.copy()

    # Extract zonal stats (list of dictionaries)
    geojson_list = rs.zonal_stats(
        awhere_grid_copy,
        src_arr,
        nodata=src_meta.get("nodata"),
        affine=src_meta.get("transform"),
        geojson_out=True,
        copy_properties=True,
        stats=zonal_stats,
    )

    # Convert list to geodataframe
    awhere_grid_rasterized = gpd.GeoDataFrame.from_features(geojson_list)

    # Return rasterized geodataframe
    return awhere_grid_rasterized


def plot_grid(
    awhere_grid, study_area, plot_title="aWhere Grid", data_source=None
):
    """Plots a administrative boundary with the
    mathching awhere grid.

    Parameters
    ----------
    awhere_grid : geopandas geodataframe
        Geodataframe containing a grid of aWhere-sized
        cells.

    study_area : geopandas geodataframe
        Geodataframe containing the study area boundary
        polygon.

    plot_title : str
        Title for the plot. Default value is 'aWhere Grid'.

    Returns
    -------
    tuple

        fig : matplotlib.figure.Figure object
            The figure object associated with the histogram.

        ax : matplotlib.axes._subplots.AxesSubplot objects
            The axes object associated with the histogram.

    Example
    -------
        >>> # Import packages
        >>> import os
        >>> import geopandas as gpd
        >>> # Define path to shapefile boundary
        >>> vt_bound_path = os.path.join(
        ...     working_directory, 'shapefiles', vermont_state_boundary.shp')
        >>> # Create aWhere grid
        >>> vt_grid, vt_bound_4326 = create_grid(
        ...     vt_bound_path, buffer_distance=0.12)
        >>> # Plot grid and boundary
        >>> fig, ax = plot_grid(vt_grid, vt_bound_4326)
    """
    # Project to WGS 84 Lat/Lon, EPSG 4326 if no CRS match
    if not study_area.crs == "epsg:4326":
        study_area_4326 = study_area.to_crs("epsg:4326")

    else:
        study_area_4326 = study_area

    # Use dark background
    with plt.style.context("dark_background"):

        # Define figure and axes
        fig, ax = plt.subplots(figsize=(20, 10))

        # Plot awhere grid and study area on same axes
        awhere_grid.plot(
            ax=ax, facecolor="none", edgecolor="#984ea3", linewidth=1.5
        )

        study_area_4326.plot(
            ax=ax, facecolor="none", edgecolor="#4daf4a", linewidth=2
        )

        # Configures axes
        ax.set_xlabel("Longitude (degrees)", fontsize=16)
        ax.set_ylabel("Latitude (degrees)", fontsize=16)
        ax.set_title(plot_title, fontsize=20)
        ax.tick_params(axis="both", which="major", labelsize=16)

        # Add caption if data source included
        if data_source:
            fig.text(
                0.5,
                0.035,
                f"Data Source: {data_source}",
                ha="center",
                fontsize=12,
            )

    # Return figure and axes
    return fig, ax


def export_grid(awhere_grid, output_path):
    """Exports an aWhere grid to the specified file format.

    Parameters
    ----------
    awhere_grid : geopandas geodataframe
        Geodataframe containing a grid of aWhere-sized
        cells.

    output_path : str
        Path to write the output file (including file
        name and extension).

    Returns
    -------
    output_message : str
        Message indicating successful export (and path)
        or error.

    Example
    -------
        >>> # Import packages
        >>> import os
        >>> import geopandas as gpd
        >>> # Define path to shapefile boundary
        >>> vt_bound_path = os.path.join(
        ...     working_directory, 'shapefiles',
        ...     vermont_state_boundary.shp')
        >>> # Create aWhere grid
        >>> vt_grid, vt_bound_4326 = create_grid(
        ...     vt_bound_path, buffer_distance=0.12)
        >>> # Define export path
        >>> # export_path = os.path.join(
        ...     working_directory, '03-processed-data',
        ...     'vt_grid.csv')
        >>> # Export grid to CSV
        >>> csv_export = export_grid(vt_grid, export_path)
        vt_grid.csv
    """
    # Determine output folder
    output_folder = os.path.dirname(output_path)

    # Raise error if output folder does not exist
    if not os.path.exists(output_folder):

        raise OSError("Directory does not exist.")

    # Extract file extension
    file_extension = output_path.split(".")[-1]

    # Define drivers for export
    drivers = {"shp": "ESRI Shapefile", "geojson": "GeoJSON", "gpkg": "GPKG"}

    # Check file extension; determine export method
    if file_extension == "csv":

        # Write to CSV
        awhere_grid.to_csv(path_or_buf=output_path, index=False)
        output_message = output_path

    elif file_extension.lower() in drivers.keys():

        # Write to shp, geojson, or gpkg
        awhere_grid.to_file(output_path, driver=drivers.get(file_extension))
        output_message = output_path

    else:
        # Raise error for unsupported file type
        raise ValueError(
            f"Invalid output format: .{file_extension}"
            "\nFormats supported: .csv, .shp, .geojson, and .gpkg"
        )

    # Return output message
    return output_message
