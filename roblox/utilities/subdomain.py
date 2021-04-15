from roblox.utilities.url import url


class Subdomain:
    def __init__(self, subdomain="www"):
        self.url = url(subdomain)

    def generate_endpoint(self, *args):
        endpoint = self.url
        for arg in args:
            endpoint += f"{arg}/"
        return endpoint
