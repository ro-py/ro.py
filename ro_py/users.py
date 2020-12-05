import requests

endpoint = "http://users.roblox.com/"


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        user_info_req = requests.get(endpoint + f"v1/users/{user_id}")
        user_info = user_info_req.json()
        self.description = user_info["description"]
        self.is_banned = user_info["isBanned"]
        self.name = user_info["name"]
        self.display_name = user_info["displayName"]

    def get_status(self):
        status_req = requests.get(endpoint + f"v1/users/{self.user_id}/status")