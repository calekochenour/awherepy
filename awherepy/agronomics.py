"""
awherepy.agronomics
===================
A module to access and retrieve aWhere agronomics data.
"""

import requests
from datetime import date
from pandas.io.json import json_normalize
import geopandas as gpd
from awherepy import AWhereAPI


class Agronomics(AWhereAPI):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):
        super(Agronomics, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = "https://api.awhere.com/v2/agronomics"

    @staticmethod
    def get_data():
        pass

    @staticmethod
    def extract_data():
        pass

    @staticmethod
    def clean_data(df, lon_lat_cols, drop_cols, name_map):
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
        crs = {"init": "epsg:4326"}

        # Rename index - possibly as option, or take care of index prior?
        # df.index.rename('date_rename', inplace=True)

        # Create copy of input dataframe; prevents altering the original
        df_copy = df.copy()

        # Convert to geodataframe
        gdf = gpd.GeoDataFrame(
            df_copy,
            crs=crs,
            geometry=gpd.points_from_xy(
                df[lon_lat_cols[0]], df[lon_lat_cols[1]]
            ),
        )

        # Add lat/lon columns to drop columns list
        drop_cols += lon_lat_cols

        # Drop columns
        gdf.drop(columns=drop_cols, axis=1, inplace=True)

        # Rename columns
        gdf.rename(columns=name_map, inplace=True)

        # Return cleaned up geodataframe
        return gdf

    @classmethod
    def api_to_gdf(cls, api_object, kwargs=None):
        """kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        api_data_df = cls.extract_data(api_data_json)

        api_data_gdf = cls.clean_data(
            api_data_df, cls.coord_cols, cls.drop_cols, cls.rename_map
        )

        return api_data_gdf


class AgronomicsLocation(Agronomics):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsLocation, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = f"{self.api_url}/locations"


class AgronomicsField(Agronomics):
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsField, self).__init__(
            api_key, api_secret, base_64_encoded_secret_key, auth_token
        )

        self.api_url = f"{self.api_url}/fields"


class AgronomicsLocationValues(AgronomicsLocation):

    # Class variables for clean_data() function
    # Single day
    day_coord_cols = ["location.longitude", "location.latitude"]

    day_drop_cols = ["pet.units", "_links.self.href"]

    day_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "pet.amount": "pet_daily_total_mm",
    }

    # Multi-day, total accumulation
    total_coord_cols = ["longitude", "latitude"]

    total_drop_cols = ["precipitation.units", "pet.units"]

    total_rename_map = {  # PPET overall?? Range total
        "gdd": "gdd_range_total_cels",
        "ppet": "ppet_range_total",  # This is accumulation of all daily PPET
        "precipitation.amount": "precip_range_total_mm",
        "pet.amount": "pet_range_total_mm",
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ["longitude", "latitude"]

    daily_drop_cols = [
        "pet.units",
        "accumulatedPrecipitation.units",
        "accumulatedPet.units",
        "_links.self.href",
    ]

    daily_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "accumulatedGdd": "gdd_rolling_total_cels",
        "accumulatedPpet": "ppet_rolling_total",
        "pet.amount": "pet_daily_total_mm",
        "accumulatedPrecipitation.amount": "precip_rolling_total_mm",
        "accumulatedPet.amount": "pet_rolling_total_mm",
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        latitude,
        longitude,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsLocationValues, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = (
            f"{self.api_url}/{self.latitude},{self.longitude}/agronomicvalues"
        )

    @staticmethod
    def get_data(
        self, start_day=date.today().strftime("%m-%d"), end_day=None, offset=0
    ):
        """Returns aWhere Forecast Agronomic Values.
        """

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_values):
        """Extracts data from the aWhere agronomic forecast
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_values.get("location").get("latitude")
        longitude = agronomic_values.get("location").get("longitude")

        # Check if more than one day
        if agronomic_values.get("dailyValues"):

            # Do these with a separate call, just like in
            #  Soil accumulation='daily'
            #  accumulation='total'

            # DAILY ACCUMULATIONS
            # Get daily forecasted accumulations
            daily_accumulation = json_normalize(
                agronomic_values.get("dailyValues")
            )

            # Add lat/lon and set date as index
            daily_accumulation["latitude"] = latitude
            daily_accumulation["longitude"] = longitude
            daily_accumulation.set_index(["date"], inplace=True)

            # TOTAL ACCUMULATION
            # Get total forecasted accumulations through all days
            total_accumulation = json_normalize(
                agronomic_values.get("accumulations")
            )

            # Get list of dates, add start/end dates, set date range as index
            dates = [
                entry.get("date")
                for entry in agronomic_values.get("dailyValues")
            ]
            total_accumulation["date_range"] = f"{dates[0]}/{dates[-1]}"
            total_accumulation["start_day"] = dates[0]
            total_accumulation["end_day"] = dates[-1]
            total_accumulation.set_index(["date_range"], inplace=True)

            # Add lat/lon
            total_accumulation["latitude"] = latitude
            total_accumulation["longitude"] = longitude

            # Put dataframes in tuple (total accumulation, daily accumulation)
            agronomics_df = (total_accumulation, daily_accumulation)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_values)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(["date"], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type="single_day", kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if value_type.lower() == "single_day":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map,
            )

        elif value_type.lower() == "multi_day":
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json
            )

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map,
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map,
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError(
                "Invalid value type. Please choose 'single_day' or"
                " 'multi_day'."
            )

        return api_data_gdf


class AgronomicsLocationNorms(AgronomicsLocation):

    # Class variables for clean_data() function

    # https://developer.awhere.com/api/reference/agronomics/norms/geolocation

    """The average ratio of Precipitation to Potential Evapotranspiration
    over the years specified. When this value is above 1, then more rain fell
    than the amount of likely water loss; if it's below 1, then more water was
    likely lost than fell as rain. P/PET is most useful when calculated for a
    range of days, as it is for this property, than for individual days."""

    # Single day
    day_coord_cols = ["location.longitude", "location.latitude"]

    day_drop_cols = ["pet.units", "_links.self.href"]

    day_rename_map = {
        "gdd.average": "gdd_daily_average_total_cels",
        "gdd.stdDev": "gdd_daily_average_total_std_dev_cels",
        "pet.average": "pet_daily_average_total_mm",
        "pet.stdDev": "pet_daily_average_total_std_dev_mm",
        "ppet.average": "ppet_daily_average_total",
        "ppet.stdDev": "ppet_daily_average_total_std_dev",
    }

    # Multi-day, total accumulation
    total_coord_cols = ["longitude", "latitude"]

    total_drop_cols = ["precipitation.units", "pet.units"]

    total_rename_map = {
        "gdd.average": "norms_gdd_average_total_cels",
        "gdd.stdDev": "norms_gdd_average_total_std_dev_cels",
        "precipitation.average": "norms_precip_average_total_mm",
        "precipitation.stdDev": "norms_precip_average_total_std_dev_mm",
        "pet.average": "norms_pet_average_total_mm",
        "pet.stdDev": "norms_pet_average_total_std_dev",
        "ppet.average": "norms_ppet_average_total",
        "ppet.stdDev": "norms_ppet_average_total_std_dev",
    }

    total_rename_map = {
        "gdd.average": "gdd_range_average_total_cels",
        "gdd.stdDev": "gdd_range_average_total_std_dev_cels",
        "precipitation.average": "precip_range_average_total_mm",
        "precipitation.stdDev": "precip_range_average_total_std_dev_mm",
        "pet.average": "pet_range_average_total_mm",
        "pet.stdDev": "pet_range_average_total_std_dev",
        # Why doesn't this match with precip_avg/pet_avg?
        # What causes this difference?
        # Is it the average of each of individual PPET daily values?
        # Seems like it
        "ppet.average": "ppet_range_daily_average",
        "ppet.stdDev": "ppet_range_daily_average_std_dev",
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ["longitude", "latitude"]

    daily_drop_cols = [
        "pet.units",
        "accumulatedPrecipitation.units",
        "accumulatedPet.units",
        "_links.self.href",
    ]

    daily_rename_map = {
        "gdd.average": "gdd_daily_average_cels",
        "gdd.stdDev": "gdd_daily_average_std_dev_cels",
        "pet.average": "pet_daily_average_mm",
        "pet.stdDev": "pet_daily_average_std_dev_mm",
        "ppet.average": "ppet_daliy_average",
        "ppet.stdDev": "ppet_daily_average_std_dev",
        "accumulatedGdd.average": "gdd_rolling_total_average",
        "accumulatedGdd.stdDev": "gdd_rolling_total_average_std_dev",
        "accumulatedPrecipitation.average": "precip_rolling_total_average_mm",
        "accumulatedPrecipitation.stdDev": "precip_rolling_total_average_std_"
        "dev_mm",
        "accumulatedPet.average": "pet_rolling_total_average_mm",
        "accumulatedPet.stdDev": "pet_rolling_total_average_std_dev_mm",
        "accumulatedPpet.average": "ppet_rolling_total_average",
        "accumulatedPpet.stdDev": "ppet_rolling_total_average_std_dev",
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        latitude,
        longitude,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsLocationNorms, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.latitude = latitude
        self.longitude = longitude
        self.api_url = (
            f"{self.api_url}/{self.latitude},{self.longitude}/agronomicnorms"
        )

    @staticmethod
    def get_data(self, start_day="01-01", end_day=None, offset=0):
        """Returns aWhere Historic Agronomic Norms.
        """

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_norms):
        """Extracts data from the aWhere agronomic norms
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_norms.get("location").get("latitude")
        longitude = agronomic_norms.get("location").get("longitude")

        # Check if more than one day
        if agronomic_norms.get("dailyNorms"):

            # DAILY ACCUMULATION NORMS
            # Get daily accumulation norms
            daily_norms = json_normalize(agronomic_norms.get("dailyNorms"))

            # Add lat/lon and set date as index
            daily_norms["latitude"] = latitude
            daily_norms["longitude"] = longitude
            daily_norms.set_index(["day"], inplace=True)

            # TOTAL ACCUMULATION NORMS
            # Get average accumulations through all days
            total_norms = json_normalize(
                agronomic_norms.get("averageAccumulations")
            )

            # Get list of dates, add start/end dates, set date range as index
            dates = [
                entry.get("day") for entry in agronomic_norms.get("dailyNorms")
            ]
            total_norms["date_range"] = f"{dates[0]}/{dates[-1]}"
            total_norms["start_day"] = dates[0]
            total_norms["end_day"] = dates[-1]
            total_norms.set_index(["date_range"], inplace=True)

            # Add lat/lon
            total_norms["latitude"] = latitude
            total_norms["longitude"] = longitude

            # Put dataframes in tuple (total norms, daily norms)
            agronomics_df = (total_norms, daily_norms)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_norms)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(["day"], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type="single_day", kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if value_type.lower() == "single_day":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map,
            )

        elif value_type.lower() == "multi_day":
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json
            )

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map,
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map,
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError(
                "Invalid value type. Please choose 'single_day' or"
                " 'multi_day'."
            )

        return api_data_gdf


class AgronomicsFieldValues(AgronomicsField):

    # Class variables for clean_data() function
    # Single day
    day_coord_cols = ["location.longitude", "location.latitude"]

    day_drop_cols = [
        "location.fieldId",
        "pet.units",
        "_links.self.href",
        "_links.curies",
        "_links.awhere:field.href",
    ]

    day_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "pet.amount": "pet_daily_total_mm",
    }

    # Multi-day, total accumulation
    total_coord_cols = ["longitude", "latitude"]

    total_drop_cols = ["precipitation.units", "pet.units"]

    total_rename_map = {  # PPET overall?? Range total
        "gdd": "gdd_range_total_cels",
        "ppet": "ppet_range_total",  # This is accumulation of all daily PPET
        "precipitation.amount": "precip_range_total_mm",
        "pet.amount": "pet_range_total_mm",
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ["longitude", "latitude"]

    daily_drop_cols = [
        "pet.units",
        "accumulatedPrecipitation.units",
        "accumulatedPet.units",
        "_links.self.href",
        "_links.curies",
        "_links.awhere:field.href",
    ]

    daily_rename_map = {
        "gdd": "gdd_daily_total_cels",
        "ppet": "ppet_daily_total",
        "accumulatedGdd": "gdd_rolling_total_cels",
        "accumulatedPpet": "ppet_rolling_total",
        "pet.amount": "pet_daily_total_mm",
        "accumulatedPrecipitation.amount": "precip_rolling_total_mm",
        "accumulatedPet.amount": "pet_rolling_total_mm",
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsFieldValues, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/agronomicvalues"

    @staticmethod
    def get_data(
        self, start_day=date.today().strftime("%m-%d"), end_day=None, offset=0
    ):
        """Returns aWhere Forecast Agronomic Values for a provided field.
        """

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_values):
        """Extracts data from the aWhere agronomic forecast
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_values.get("location").get("latitude")
        longitude = agronomic_values.get("location").get("longitude")

        # Check if more than one day
        if agronomic_values.get("dailyValues"):

            # Do these with a separate call, just like in
            #  Soil accumulation='daily'
            #  accumulation='total'

            # DAILY ACCUMULATIONS
            # Get daily forecasted accumulations
            daily_accumulation = json_normalize(
                agronomic_values.get("dailyValues")
            )

            # Add lat/lon and set date as index
            daily_accumulation["latitude"] = latitude
            daily_accumulation["longitude"] = longitude
            daily_accumulation.set_index(["date"], inplace=True)

            # TOTAL ACCUMULATION
            # Get total forecasted accumulations through all days
            total_accumulation = json_normalize(
                agronomic_values.get("accumulations")
            )

            # Get list of dates, add start/end dates, set date range as index
            dates = [
                entry.get("date")
                for entry in agronomic_values.get("dailyValues")
            ]
            total_accumulation["date_range"] = f"{dates[0]}/{dates[-1]}"
            total_accumulation["start_day"] = dates[0]
            total_accumulation["end_day"] = dates[-1]
            total_accumulation.set_index(["date_range"], inplace=True)

            # Add lat/lon
            total_accumulation["latitude"] = latitude
            total_accumulation["longitude"] = longitude

            # Put dataframes in tuple (total accumulation, daily accumulation)
            agronomics_df = (total_accumulation, daily_accumulation)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_values)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(["date"], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type="single_day", kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if value_type.lower() == "single_day":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map,
            )

        elif value_type.lower() == "multi_day":
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json
            )

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map,
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map,
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError(
                "Invalid value type. Please choose 'single_day' or"
                " 'multi_day'."
            )

        return api_data_gdf


class AgronomicsFieldNorms(AgronomicsField):

    # Class variables for clean_data() function

    # https://developer.awhere.com/api/reference/agronomics/norms/geolocation

    """The average ratio of Precipitation to Potential Evapotranspiration
    over the years specified. When this value is above 1, then more rain fell
    than the amount of likely water loss; if it's below 1, then more water was
    likely lost than fell as rain. P/PET is most useful when calculated for a
    range of days, as it is for this property, than for individual days."""

    # Single day
    day_coord_cols = ["location.longitude", "location.latitude"]

    day_drop_cols = [
        "location.fieldId",
        "pet.units",
        "_links.self.href",
        "_links.curies",
        "_links.awhere:field.href",
    ]

    day_rename_map = {
        "gdd.average": "gdd_daily_average_total_cels",
        "gdd.stdDev": "gdd_daily_average_total_std_dev_cels",
        "pet.average": "pet_daily_average_total_mm",
        "pet.stdDev": "pet_daily_average_total_std_dev_mm",
        "ppet.average": "ppet_daily_average_total",
        "ppet.stdDev": "ppet_daily_average_total_std_dev",
    }

    # Multi-day, total accumulation
    total_coord_cols = ["longitude", "latitude"]

    total_drop_cols = ["precipitation.units", "pet.units"]

    total_rename_map = {
        "gdd.average": "gdd_range_average_total_cels",
        "gdd.stdDev": "gdd_range_average_total_std_dev_cels",
        "precipitation.average": "precip_range_average_total_mm",
        "precipitation.stdDev": "precip_range_average_total_std_dev_mm",
        "pet.average": "pet_range_average_total_mm",
        "pet.stdDev": "pet_range_average_total_std_dev",
        # Why doesn't this match with precip_avg/pet_avg?
        # What causes this difference?
        # Is it the average of each of individual PPET daily values?
        # Seems like it
        "ppet.average": "ppet_range_daily_average",
        "ppet.stdDev": "ppet_range_daily_average_std_dev",
    }

    # Multi-day, daily accumulation
    daily_coord_cols = ["longitude", "latitude"]

    daily_drop_cols = [
        "pet.units",
        "accumulatedPrecipitation.units",
        "accumulatedPet.units",
        "_links.self.href",
        "_links.curies",
        "_links.awhere:field.href",
    ]

    daily_rename_map = {
        "gdd.average": "gdd_daily_average_cels",
        "gdd.stdDev": "gdd_daily_average_std_dev_cels",
        "pet.average": "pet_daily_average_mm",
        "pet.stdDev": "pet_daily_average_std_dev_mm",
        "ppet.average": "ppet_daliy_average",
        "ppet.stdDev": "ppet_daily_average_std_dev",
        "accumulatedGdd.average": "gdd_rolling_total_average",
        "accumulatedGdd.stdDev": "gdd_rolling_total_average_std_dev",
        "accumulatedPrecipitation.average": "precip_rolling_total_average_mm",
        "accumulatedPrecipitation.stdDev": "precip_rolling_total_average_std_"
        "dev_mm",
        "accumulatedPet.average": "pet_rolling_total_average_mm",
        "accumulatedPet.stdDev": "pet_rolling_total_average_std_dev_mm",
        "accumulatedPpet.average": "ppet_rolling_total_average",
        "accumulatedPpet.stdDev": "ppet_rolling_total_average_std_dev",
    }

    # Define lat/lon when intitializing class; no need to repeat for lat/lon
    #  in get_data() because it is already programmed into api_url
    def __init__(
        self,
        api_key,
        api_secret,
        field_id,
        base_64_encoded_secret_key=None,
        auth_token=None,
        api_url=None,
    ):

        super(AgronomicsFieldNorms, self).__init__(
            api_key,
            api_secret,
            base_64_encoded_secret_key,
            auth_token,
            api_url,
        )

        self.field_id = field_id
        self.api_url = f"{self.api_url}/{self.field_id}/agronomicnorms"

    @staticmethod
    def get_data(self, start_day="01-01", end_day=None, offset=0):
        """Returns aWhere Historic Agronomic Norms.
        """

        # Setup the HTTP request headers
        auth_headers = {"Authorization": f"Bearer {self.auth_token}"}

        # Perform the HTTP request to obtain the norms for the Field
        # Define URL variants
        url_single_day = f"{self.api_url}/{start_day}"
        url_multiple_days = (
            f"{self.api_url}/{start_day},{end_day}?limit=10&offset={offset}"
        )

        # Get single day norms or date range
        response = (
            requests.get(url_multiple_days, headers=auth_headers)
            if end_day
            else requests.get(url_single_day, headers=auth_headers)
        )

        # Return the norms
        return response.json()

    @staticmethod
    def extract_data(agronomic_norms):
        """Extracts data from the aWhere agronomic norms
        data in JSON format.
        """
        # Extract lat/lon
        latitude = agronomic_norms.get("location").get("latitude")
        longitude = agronomic_norms.get("location").get("longitude")

        # Check if more than one day
        if agronomic_norms.get("dailyNorms"):

            # DAILY ACCUMULATION NORMS
            # Get daily accumulation norms
            daily_norms = json_normalize(agronomic_norms.get("dailyNorms"))

            # Add lat/lon and set date as index
            daily_norms["latitude"] = latitude
            daily_norms["longitude"] = longitude
            daily_norms.set_index(["day"], inplace=True)

            # TOTAL ACCUMULATION NORMS
            # Get average accumulations through all days
            total_norms = json_normalize(
                agronomic_norms.get("averageAccumulations")
            )

            # Get list of dates, add start/end dates, set date range as index
            dates = [
                entry.get("day") for entry in agronomic_norms.get("dailyNorms")
            ]
            total_norms["date_range"] = f"{dates[0]}/{dates[-1]}"
            total_norms["start_day"] = dates[0]
            total_norms["end_day"] = dates[-1]
            total_norms.set_index(["date_range"], inplace=True)

            # Add lat/lon
            total_norms["latitude"] = latitude
            total_norms["longitude"] = longitude

            # Put dataframes in tuple (total norms, daily norms)
            agronomics_df = (total_norms, daily_norms)

        # Single day
        else:
            agronomics_df = json_normalize(agronomic_norms)
            # agronomics_df['latitude'] = latitude
            # agronomics_df['longitude'] = longitude
            agronomics_df.set_index(["day"], inplace=True)

        return agronomics_df

    @classmethod
    def api_to_gdf(cls, api_object, value_type="single_day", kwargs=None):
        """
        value_type can be 'single_day' or 'multi_day'.

        kwargs is a dictionary that provides values beyond the default;
        unpack dictionary if it exists

        kwargs are the parameters to get_data() method

        kwargs={'start_day': '03-04', 'end_day': '03-07', 'offset': 2}
        """
        api_data_json = (
            api_object.get_data(**kwargs) if kwargs else api_object.get_data()
        )

        if value_type.lower() == "single_day":
            api_data_df = cls.extract_data(api_data_json)

            api_data_gdf = cls.clean_data(
                api_data_df,
                cls.day_coord_cols,
                cls.day_drop_cols,
                cls.day_rename_map,
            )

        elif value_type.lower() == "multi_day":
            api_data_df_total, api_data_df_daily = cls.extract_data(
                api_data_json
            )

            api_data_gdf_total = cls.clean_data(
                api_data_df_total,
                cls.total_coord_cols,
                cls.total_drop_cols,
                cls.total_rename_map,
            )

            api_data_gdf_daily = cls.clean_data(
                api_data_df_daily,
                cls.daily_coord_cols,
                cls.daily_drop_cols,
                cls.daily_rename_map,
            )

            api_data_gdf = (api_data_gdf_total, api_data_gdf_daily)

        else:
            raise ValueError(
                "Invalid value type. Please choose 'single_day' or"
                " 'multi_day'."
            )

        return api_data_gdf
