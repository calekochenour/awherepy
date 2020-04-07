import pandas as pd
from pandas.io.json import json_normalize


def extract_forecast_main_data(forecast):
    """Extract aWhere forecast data and returns
    it in a pandas dataframe.
    """
    # Initialize lists to store forecast
    forecast_main_list = []

    # Loop through each row in the top-level flattened dataframe
    for index, row in json_normalize(forecast.get('forecasts')).iterrows():

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


def extract_forecast_soil_temp(forecast):
    """Extract aWhere forecast soil temperature
    data and returns it in a pandas dataframe.
    """
    # Initialize lists to store soil temp dataframes
    forecast_soil_temp_list = []

    # Loop through each row in the top-level flattened dataframe
    for index, row in json_normalize(forecast.get('forecasts')).iterrows():

        # Extract date, lat, lon for insertion into lower-level dataframe outputs
        date = row['date']
        lat = row['location.latitude']
        lon = row['location.longitude']

        # Get soil temperature data
        forecast_soil_temp = row['forecast'][0].get('soilTemperatures')

        # Flatten data into dataframe
        forecast_soil_temp_norm = json_normalize(forecast_soil_temp)

        # Assign date, lat/lon to dataframe
        forecast_soil_temp_norm['date'] = date
        forecast_soil_temp_norm['latitude'] = lat
        forecast_soil_temp_norm['longitude'] = lon

        # Create multi-index dataframe for date and soil depth (rename depth columns? rather long)
        soil_temp_multi_index = forecast_soil_temp_norm.set_index(
            ['date', 'depth'])

        # Add dataframe to list of dataframes
        forecast_soil_temp_list.append(soil_temp_multi_index)

    # Return merged lists of dataframes into a single dataframe
    return pd.concat(forecast_soil_temp_list)


def extract_forecast_soil_moisture(forecast):
    """Extract aWhere forecast soil moisture
    data and returns it in a pandas dataframe.
    """
    # Initialize lists to store soil moisture dataframes
    forecast_soil_moisture_list = []

    # Loop through each row in the top-level flattened dataframe
    for index, row in json_normalize(forecast.get('forecasts')).iterrows():

        # Extract date, lat, lon for insertion into lower-level dataframe outputs
        date = row['date']
        lat = row['location.latitude']
        lon = row['location.longitude']

        # Get soil moisture data
        forecast_soil_moisture = row['forecast'][0].get('soilMoisture')

        # Flatten data into dataframe
        forecast_soil_moisture_norm = json_normalize(forecast_soil_moisture)

        # Assign date, lat/lon to dataframe
        forecast_soil_moisture_norm['date'] = date
        forecast_soil_moisture_norm['latitude'] = lat
        forecast_soil_moisture_norm['longitude'] = lon

        # Create multi-index dataframe for date and soil depth (rename depth columns? rather long)
        soil_moisture_multi_index = forecast_soil_moisture_norm.set_index([
            'date', 'depth'])

        # Add dataframe to list of dataframes
        forecast_soil_moisture_list.append(soil_moisture_multi_index)

    # Return merged lists of dataframes into a single dataframe
    return pd.concat(forecast_soil_moisture_list)
