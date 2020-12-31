endpoint = "https://groups.roblox.com"


class Role:
    """
    Represents a role
    This is only available for authenticated clients as it cannot be accessed otherwise.

    Parameters
    ----------
    requests : ro_py.utilities.requests.Requests
            Requests object to use for API requests.
    group : ro_py.groups.Group
            Group the role belongs to.
    role_data : dict
            Dictionary containing role information.
    """
    def __init__(self, requests, group, role_data):
        self.requests = requests
        self.group = group
        self.id = role_data['id']
        self.name = role_data['name']
        self.description = role_data['description']
        self.rank = role_data['rank']
        self.member_count = role_data['memberCount']

    async def update(self):
        update_req = await self.requests.get(
            url=endpoint + f"/v1/groups/{self.group.id}/roles"
        )
        data = update_req.json()
        for role in data['roles']:
            if role['id'] == self.id:
                self.name = role['name']
                self.description = role['description']
                self.rank = role['rank']
                self.member_count = role['memberCount']
                break

    async def edit(self, name=None, description=None, rank=None):
        edit_req = await self.requests.patch(
            url=endpoint + f"/v1/groups/{self.group.id}/rolesets/{self.id}",
            data={
                "description": description if description else self.description
                "name": name if name else self.name,
                "rank": rank if rank else self.rank
            }
        )
        return edit_req.status_code == 200

    # TODO:
    async def edit_permissions(self):
        pass
