class RobloxBadge:
    def __init__(self, roblox_badge_data):
        self.id = roblox_badge_data["id"]
        self.name = roblox_badge_data["name"]
        self.description = roblox_badge_data["description"]
        self.image_url = roblox_badge_data["imageUrl"]
