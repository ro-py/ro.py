root_site = "roblox.com"


def url(path="www"):
    if path:
        return f"https://{path}.{root_site}/"
    else:
        return f"https://{root_site}"
