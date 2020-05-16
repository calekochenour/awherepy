def compare_forecast(forecast_1, forecast_2):
    """Compares forecast data (full data) to determine
    if the data is the same.

    Meant for comparing aWhere API fields at the same
    location but with different {acres} parameters.
    """

    is_equal = True if forecast_1.get('forecasts')[0].get(
        'forecast') == forecast_2.get('forecasts')[0].get(
        'forecast') else False

    return is_equal


def compare_historical(historical_1, historical_2):
    """Compares subset of historical data (precipitation)
    to determine if the data is the same.

    Meant for comparing aWhere API fields at the same
    location but with different {acres} parameters.
    """

    is_equal = True if historical_1.get('norms')[0].get(
        'precipitation') == historical_2.get('norms')[0].get(
        'precipitation') else False

    return is_equal


def compare_observed(observed_1, observed_2):
    """Compares subset of observed data (precipitation)
    to determine if the data is the same.

    Meant for comparing aWhere API fields at the same
    location but with different {acres} parameters.
    """

    is_equal = True if observed_1.get('observations')[0].get(
        'precipitation') == observed_2.get('observations')[0].get(
        'precipitation') else False

    return is_equal
