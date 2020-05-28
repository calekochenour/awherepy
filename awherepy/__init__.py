"""

Base class for authenticating to the the aWhere API.

"""

import base64
import requests


class AWhereAPI:
    def __init__(
        self,
        api_key,
        api_secret,
        base_64_encoded_secret_key=None,
        auth_token=None,
        # api_url="https://api.awhere.com/v2/"
    ):
        # Define authorization information
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_64_encoded_secret_key = self.encode_secret_and_key(
            self.api_key, self.api_secret
        )
        self.auth_token = self.get_oauth_token(self.base_64_encoded_secret_key)

    def encode_secret_and_key(self, key, secret):
        """
        Docs:
            http://developer.awhere.com/api/authentication
        Returns:
            Returns the base64-encoded {key}:{secret} combination,
            seperated by a colon.
        """
        # Base64 Encode the Secret and Key
        key_secret = f"{key}:{secret}"

        encoded_key_secret = base64.b64encode(
            bytes(key_secret, "utf-8")
        ).decode("ascii")

        return encoded_key_secret

    def get_oauth_token(self, encoded_key_secret):
        """
        Demonstrates how to make a HTTP POST request to obtain an OAuth Token

        Docs:
            http://developer.awhere.com/api/authentication

        Returns:
            The access token provided by the aWhere API
        """
        # Define authorization parameters
        auth_url = "https://api.awhere.com/oauth/token"

        auth_headers = {
            "Authorization": f"Basic {encoded_key_secret}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        body = "grant_type=client_credentials"

        # Perform HTTP request for OAuth Token
        response = requests.post(auth_url, headers=auth_headers, data=body)

        # Return access token
        return response.json()["access_token"]
