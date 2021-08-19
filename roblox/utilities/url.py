root_site = "roblox.com"


def url(subdomain="www") -> str:
    """
    Generates a url using a path

    Parameters
    ----------
    subdomain : str
        The path of the url

    Returns
    -------
    str
    """
    if subdomain:
        return f"https://{subdomain}.{root_site}/"
    else:
        return f"https://{root_site}"

