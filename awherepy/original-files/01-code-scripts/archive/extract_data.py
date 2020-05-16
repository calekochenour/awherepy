import pandas as pd
from pandas.io.json import json_normalize


def extract_forecast_main_data(forecast):
    """Extract aWhere forecast data and returns
    it in a pandas dataframe.
    """
    # Initialize lists to store forecast
    forecast_main_list = []

    # Check if more than one day
    if forecast.get('forecasts'):
        forecast_iterator = json_normalize(forecast.get('forecasts'))

    # Single day
    else:
        forecast_iterator = json_normalize(forecast)

    # Loop through each row in the top-level flattened dataframe
    for index, row in forecast_iterator.iterrows():

        # Extract date, lat, lon for insertion into lower-level dataframe outputs
        date = row['date']
        lat = row['location.latitude']
        lon = row['location.longitude']

        # Extract the main forecast from the top-level dataframe
        forecast = row['forecast']

        # Faltten data into dataframe
        forecast_norm = json_normalize(forecast)

        # Drop soil moisture and soil temperature columns
        #  (will be extracted as indivdiual dataframes)
        forecast_norm.drop(columns=[
            'soilTemperatures',
            'soilMoisture',
        ],
            axis=1, inplace=True)
        # Assign date, lat/lon to dataframe
        forecast_norm['date'] = date
        forecast_norm['latitude'] = lat
        forecast_norm['longitude'] = lon

        # Set date as index
        forecast_norm.set_index(['date'], inplace=True)

        # Add the dataframe to a list of dataframes
        forecast_main_list.append(forecast_norm)

    # Return merged lists of dataframes into a single dataframe
    return pd.concat(forecast_main_list)


def extract_forecast_soil(forecast):
    """Extract aWhere forecast soil
    data and returns it in a pandas dataframe.
    """
    # Initialize lists to store soil dataframes
    forecast_soil_list = []

    # Check if more than one day
    if forecast.get('forecasts'):
        forecast_iterator = json_normalize(forecast.get('forecasts'))

    # Single day
    else:
        forecast_iterator = json_normalize(forecast)

    # Loop through each row in the top-level flattened dataframe
    for index, row in forecast_iterator.iterrows():

        # Extract date, lat, lon for insertion into lower-level dataframe outputs
        date = row['date']
        lat = row['location.latitude']
        lon = row['location.longitude']

        # Get soil temperature data
        forecast_soil_temp = row['forecast'][0].get('soilTemperatures')
        forecast_soil_moisture = row['forecast'][0].get('soilMoisture')

        # Flatten data into dataframe
        forecast_soil_temp_df = json_normalize(forecast_soil_temp)
        forecast_soil_moisture_df = json_normalize(forecast_soil_moisture)

        # Combine temperature and moisture
        forecast_soil_df = forecast_soil_temp_df.merge(
            forecast_soil_moisture_df, on='depth', suffixes=('_temp', '_moisture'))

        # Assign date, lat/lon to dataframe
        forecast_soil_df['date'] = date
        forecast_soil_df['latitude'] = lat
        forecast_soil_df['longitude'] = lon

        # Shorten depth values to numerics (will be used in MultiIndex)
        forecast_soil_df['depth'] = forecast_soil_df['depth'].apply(lambda x: x[0:-15])

        # Rename depth prior to indexing
        forecast_soil_df.rename(columns={'depth': 'ground_depth_m'}, inplace=True)

        # Create multi-index dataframe for date and soil depth (rename depth columns? rather long)
        soil_multi_index = forecast_soil_df.set_index(
            ['date', 'ground_depth_m'])

        # Add dataframe to list of dataframes
        forecast_soil_list.append(soil_multi_index)

    # Return merged lists of dataframes into a single dataframe
    return pd.concat(forecast_soil_list)


def extract_historic_norms(historic_norms):
    """Creates a dataframe from a JSON-like
    dictionary of aWhere historic norm data.

    Handles both single-day norms and multiple days.

    Parameters
    ----------
    historic_norms : dict
        aWhere historic norm data in dictionary format.

    Returns
    -------
    historic_norms_df : pandas dataframe
        Flattened dataframe version of historic norms.
    """
    # Check if multiple entries (days) are in norms
    if historic_norms.get('norms'):
        # Flatten to dataframe
        historic_norms_df = json_normalize(historic_norms.get('norms'))

    # Single-day norm
    else:
        # Flatten to dataframe
        historic_norms_df = json_normalize(historic_norms)

    # Set day as index
    historic_norms_df.set_index('day', inplace=True)

    # Drop unnecessary columns
    historic_norms_df.drop(
        columns=[
            '_links.self.href',
            '_links.curies',
            '_links.awhere:field.href'],
        axis=1, inplace=True)

    # Return dataframe
    return historic_norms_df


def extract_observed_weather(observed_weather):
    """Creates a dataframe from a JSON-like
    dictionary of aWhere observed weather data.

    Parameters
    ----------
    observed_weather : dict
        aWhere historic norm data in dictionary format.

    Returns
    -------
    observed_weather_df : pandas dataframe
        Flattened dataframe version of historic norms.
    """
    # Check if multiple entries (days) are in observed
    if observed_weather.get('observations'):
        # Flatten to dataframe
        observed_weather_df = json_normalize(observed_weather.get('observations'))

    # Single-day observed
    else:
        # Flatten to dataframe
        observed_weather_df = json_normalize(observed_weather)

    # Set date as index
    observed_weather_df.set_index('date', inplace=True)

    # Drop unnecessary columns
    observed_weather_df.drop(
        columns=[
            '_links.self.href',
            '_links.curies',
            '_links.awhere:field.href'],
        axis=1, inplace=True)

    # Return dataframe
    return observed_weather_df


if __name__ == '__main__':
    # Imports
    import os
    import pandas as pd
    from pandas.io.json import json_normalize
    from awhere import AWhereAPI

    # Get API key and secret
    api_key = os.environ.get('AWHERE_API_KEY')
    api_secret = os.environ.get('AWHERE_API_SECRET')

    # Create aWhere object
    awhere = AWhereAPI(api_key, api_secret)

    # Get forecast, historic norms, and observed weather
    field = 'Colorado-Test-1'
    forecast = awhere.get_weather_forecast(field)
    norms = awhere.get_weather_norms(field, '05-05')
    observed = awhere.get_weather_observed(field)

    # Create dataframes
    forecast_main_df = extract_forecast_main_data(forecast)
    forecast_soil_temp_df = extract_forecast_soil_temp(forecast)
    forecast_soil_moisture_df = extract_forecast_soil_moisture(forecast)
    norms_df = extract_historic_norms(norms)
    observed_df = extract_observed_weather(observed)
