import requests

endpoint = "https://users.roblox.com/"


class User:
    def __init__(self, user_id):
        self.id = user_id
        user_info_req = requests.get(endpoint + f"v1/users/{self.id}")
        user_info = user_info_req.json()
        self.description = user_info["description"]
        self.is_banned = user_info["isBanned"]
        self.name = user_info["name"]
        self.display_name = user_info["displayName"]
        has_premium_req = requests.get(f"https://premiumfeatures.roblox.com/v1/users/{self.id}/validate-membership")
        self.has_premium = has_premium_req

    def get_status(self):
        status_req = requests.get(endpoint + f"v1/users/{self.id}/status")
        return status_req.json()["status"]
