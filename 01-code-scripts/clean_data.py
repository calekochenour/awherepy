import geopandas as gpd


def clean_dataframe(df, lon_lat_cols, drop_cols, name_map):
    """Converts dataframe to geodataframe,
    drops unnecessary columns, and renames
    columns.

    Parameters
    ----------
    df : dataframe
        Input dataframe.

    lon_lat_cols : list
        List containing the column name for longitude (list[0])
        and latitude (list[1]) attributes.

    drop_cols : list (of str)
        List of column names to be dropped.

    name_map : dict
        Dictionaty mapping old columns names (keys)
        to new column names (values).

    Returns
    -------
    gdf : geodataframe
        Cleaned geodataframe.

    Example
    -------
    """
    # Define CRS (EPSG 4326) - make this a parameter?
    crs = {'init': 'epsg:4326'}

    # Rename index - possibly as option, or take care of index prior?
    #df.index.rename('date_rename', inplace=True)

    # Convert to geodataframe
    gdf = gpd.GeoDataFrame(
        df, crs=crs, geometry=gpd.points_from_xy(
            df[lon_lat_cols[0]],
            df[lon_lat_cols[1]])
    )

    # Add lat/lon columns to drop columns list
    drop_cols += lon_lat_cols

    # Drop columns
    gdf.drop(columns=drop_cols, axis=1, inplace=True)

    # Rename columns
    gdf.rename(columns=name_map, inplace=True)

    # Return cleaned up geodataframe
    return gdf


# Global variables
forecast_lon_lat_cols = ['longitude', 'latitude']

forecast_main_drop_cols = [
    'temperatures.units', 'precipitation.units',
    'solar.units', 'wind.units', 'dewPoint.units'
]

forecast_main_mapping = {
    'startTime': 'start_time',
    'endTime': 'end_time',
    'conditionsCode': 'conditions_code',
    'conditionsText': 'conditions_text',
    'temperatures.max': 'temp_max_cels',
    'temperatures.min': 'temp_min_cels',
    'precipitation.chance': 'precip_chance_%',
    'precipitation.amount': 'precip_amount_mm',
    'sky.cloudCover': 'sky_cloud_cover_%',
    'sky.sunshine': 'sky_sunshine_%',
    'solar.amount': 'solar_energy_w_h_per_m2',
    'relativeHumidity.average': 'rel_humidity_avg_%',
    'relativeHumidity.max': 'rel_humidity_max_%',
    'relativeHumidity.min': 'rel_humidity_min_%',
    'wind.average': 'wind_avg_m_per_sec',
    'wind.max': 'wind_max_m_per_sec',
    'wind.min': 'wind_min_m_per_sec',
    'wind.bearing': 'wind_bearing_deg',
    'wind.direction': 'wind_direction_compass',
    'dewPoint.amount': 'dew_point_cels'
}
