"""

This file houses functions and classes that pertain to the Roblox status page (at status.roblox.com)
I don't know if this is really that useful, but I was able to find the status API endpoint by looking in the status
page source and some of the status.io documentation.

"""

import iso8601

endpoint = "https://4277980205320394.hostedstatus.com/1.0/status/59db90dbcdeb2f04dadcf16d"


class RobloxStatusContainer:
    """
    Represents a tab or item in a tab on the Roblox status site.
    The tab items are internally called "containers" so that's what I call them here.
    I don't see any difference between the data in tabs and data in containers, so I use the same object here.
    """
    def __init__(self, container_data):
        self.id = container_data["id"]
        self.name = container_data["name"]
        self.updated = iso8601.parse_date(container_data["updated"])
        self.status = container_data["status"]
        self.status_code = container_data["status_code"]


class RobloxStatusOverall:
    """
    Represents the overall status on the Roblox status site.
    """
    def __init__(self, overall_data):
        self.updated = iso8601.parse_date(overall_data["updated"])
        self.status = overall_data["status"]
        self.status_code = overall_data["status_code"]


class RobloxStatus:
    def __init__(self, requests):
        self.requests = requests

        self.overall = None
        self.user = None
        self.player = None
        self.creator = None

        self.update()

    def update(self):
        status_req = self.requests.get(
            url=endpoint
        )
        status_data = status_req.json()["result"]

        self.overall = RobloxStatusOverall(status_data["status_overall"])
        self.user = RobloxStatusContainer(status_data["status"][0])
        self.player = RobloxStatusContainer(status_data["status"][1])
        self.creator = RobloxStatusContainer(status_data["status"][2])
