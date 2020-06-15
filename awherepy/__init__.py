"""

Base class for authenticating to the aWhere API.

"""

import base64
import requests as rq


def get_oauth_token(key, secret):
    """Returns an OAuth Token used to authenticate to the
    aWhere API if a valid key and secret are provided.

    API reference: http://developer.awhere.com/api/authentication

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    Returns
    -------
    access_token : str
        Access token created from the API key and secret.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Get OAuth token
        >>> auth_token = aw.get_oauth_token(awhere_api_key, awhere_api_secret)
    """
    # Base64 Encode the API key/secret pair
    encoded_key_secret = base64.b64encode(
        bytes(f"{key}:{secret}", "utf-8")
    ).decode("ascii")

    # Define authorization parameters for HTTP request
    auth_url = "https://api.awhere.com/oauth/token"

    auth_headers = {
        "Authorization": f"Basic {encoded_key_secret}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    auth_body = "grant_type=client_credentials"

    # Request OAuth Token
    response = rq.post(url=auth_url, headers=auth_headers, data=auth_body)

    # Get access token
    access_token = response.json().get("access_token")

    # Return access token
    return access_token


def valid_credentials(key, secret):
    """Returns True if aWhere API credentials are valid, else False.

    Parameters
    ----------
    key : str
        API key for a valid aWhere API application.

    secret : str
        API secret for a valid aWhere API application.

    Returns
    -------
    valid : bool
        Boolean indicating True if API credentials are valid, else false.

    Example
    -------
        >>> # Imports
        >>> import os
        >>> import awherepy as aw
        >>> # Get aWhere API key and secret
        >>> awhere_api_key = os.environ.get('AWHERE_API_KEY')
        >>> awhere_api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Check validity of credentials and get OAuth token
        >>> if aw.valid_credentials(awhere_api_key, awhere_api_secret):
        ...     auth_token = aw.get_oauth_token(
        ...         awhere_api_key, awhere_api_secret
        ...     )
    """
    # Get OAuth token
    token = get_oauth_token(key, secret)

    # Check for validity
    valid = False if token is None else True

    # Return valid
    return valid
    # return False if get_oauth_token(key, secret) is None else True
