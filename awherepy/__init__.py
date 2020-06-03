"""

Base class for authenticating to the aWhere API.

"""

import base64
import requests as rq


def get_oauth_token(key, secret):
    """Returns an OAuth Token used to authenticate to the
    aWhere API if a valid key and secret are provided.

    Docs:
        http://developer.awhere.com/api/authentication

    Returns:
        The access token provided by the aWhere API
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
    """Returns True if credentials are valid, else False.

    Checks if encoding the provided key and secret returns
    a value (not NoneType).
    """
    # Get OAuth token
    token = get_oauth_token(key, secret)

    # Check for validity
    valid = False if token is None else True

    # Return valid
    return valid
    # return False if get_oauth_token(key, secret) is None else True
