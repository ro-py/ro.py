root_site = "roblox.com"


def url(path="www") -> str:
    """
    Generates a url using a path

    Parameters
    ----------
    path : str
        The path of the url

    Returns
    -------
    str
    """
    if path:
        return f"https://{path}.{root_site}/"
    else:
        return f"https://{root_site}"
