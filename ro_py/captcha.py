"""

This file houses functions and classes that pertain to the Roblox captcha.

"""


class UnsolvedLoginCaptcha:
    def __init__(self, data, pkey):
        self.pkey = pkey
        self.token = data["token"]
        self.url = f"https://roblox-api.arkoselabs.com/fc/api/nojs/" \
                   f"?pkey={pkey}" \
                   f"&session={self.token.split('|')[0]}" \
                   f"&lang=en"
        self.challenge_url = data["challenge_url"]
        self.challenge_url_cdn = data["challenge_url_cdn"]
        self.noscript = data["noscript"]


class UnsolvedCaptcha:
    def __init__(self, pkey):
        self.pkey = pkey
        self.url = f"https://roblox-api.arkoselabs.com/fc/api/nojs/" \
                   f"?pkey={pkey}" \
                   f"&lang=en"


class CaptchaMetadata:
    def __init__(self, data):
        self.fun_captcha_public_keys = data["funCaptchaPublicKeys"]
