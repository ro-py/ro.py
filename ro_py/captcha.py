"""

This file houses functions and classes that pertain to the Roblox captcha.

"""


class UnsolvedCaptcha:
    def __init__(self, data, pkey):
        self.token = data["token"]
        self.url = f"https://roblox-api.arkoselabs.com/fc/api/nojs/?pkey={pkey}&session={self.token.split('|')[0]}&lang=en-gb"
        self.challenge_url = data["challenge_url"]
        self.challenge_url_cdn = data["challenge_url_cdn"]
        self.noscript = data["noscript"]
