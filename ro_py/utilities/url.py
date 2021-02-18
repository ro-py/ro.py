root_site = "sitetest1.roblox.com"


def url(path="www"):
    if path:
        return f"https://{path}.{root_site}/"
    else:
        return f"https://{root_site}"
