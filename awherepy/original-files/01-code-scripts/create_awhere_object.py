def create_awhere(api_key, api_secret):
    """Creates aWhere object if the API key and
    secret are valid. Returns False otherwise.

    Parameters
    ----------
    api_key : str
        API key for aWhere app.

    api_secret : str
        API secret for aWhere app.

    Returns
    -------
    aWhere : AWhereAPI object
        Object of class aWhereAPI that corresponds to
        the aWhere app associated with the provided
        API key and secret.

    Example
    -------
        >>> # Import os module and AWhereAPI class
        >>> import os
        >>> from awhere import AWhereAPI
        >>> # Get API key and secret from local environment variable
        >>> api_key = os.environ.get('AWHERE_API_KEY')
        >>> api_secret = os.environ.get('AWHERE_API_SECRET')
        >>> # Create aWhereAPI object
        >>> awhere_object = create_awhere(api_key, api_secret)
        SUCCESS: Valid authentication credentials. aWhere object created.
    """
    # Create aWhere object with key/secret
    try:
        aWhere = AWhereAPI(api_key, api_secret)

    # Catch KeyError (invalid key or secret)
    except KeyError:
        print("ERROR: Invalid API key or API secret.")
        aWhere = False

    # Catch other exceptions
    except Exception as error:
        print(f"ERROR: {error}")
        aWhere = False

    # Run if no exceptions
    else:
        print(
            "SUCCESS: Valid authentication credentials. aWhere object created."
        )

    return aWhere


if __name__ == "__main__":
    # Import os module and AWhereAPI class
    import os
    from awhere import AWhereAPI

    # Get API key and secret
    api_key = os.environ.get("AWHERE_API_KEY")
    api_secret = os.environ.get("AWHERE_API_SECRET")

    # Create aWhere object
    awhere = create_awhere(api_key, api_secret)
