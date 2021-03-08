"""

This file contains classes and functions related to Roblox roles.

"""


from ro_py.utilities.url import url
endpoint = url("groups")


class RolePermissions:
    """
    Represents role permissions.
    """
    view_wall = None
    post_to_wall = None
    delete_from_wall = None
    view_status = None
    post_to_status = None
    change_rank = None
    invite_members = None
    remove_members = None
    manage_relationships = None
    view_audit_logs = None
    spend_group_funds = None
    advertise_group = None
    create_items = None
    manage_items = None
    manage_group_games = None


def get_rp_names(rp):
    """
    Converts permissions into something Roblox can read.

    Parameters
    ----------
    rp : ro_py.roles.RolePermissions

    Returns
    -------
    dict
    """
    return {
        "viewWall": rp.view_wall,
        "PostToWall": rp.post_to_wall,
        "deleteFromWall": rp.delete_from_wall,
        "viewStatus": rp.view_status,
        "postToStatus": rp.post_to_status,
        "changeRank": rp.change_rank,
        "inviteMembers": rp.invite_members,
        "removeMembers": rp.remove_members,
        "manageRelationships": rp.manage_relationships,
        "viewAuditLogs": rp.view_audit_logs,
        "spendGroupFunds": rp.spend_group_funds,
        "advertiseGroup": rp.advertise_group,
        "createItems": rp.create_items,
        "manageItems": rp.manage_items,
        "manageGroupGames": rp.manage_group_games
    }


class Role:
    """
    Represents a role

    Parameters
    ----------
    requests : ro_py.utilities.requests.Requests
            Requests object to use for API requests.
    group : ro_py.groups.Group
            Group the role belongs to.
    role_data : dict
            Dictionary containing role information.
    """
    def __init__(self, cso, group, role_data):
        self.cso = cso
        self.requests = cso.requests
        self.group = group
        self.id = role_data['id']
        self.name = role_data['name']
        self.description = role_data.get('description')
        self.rank = role_data['rank']
        self.member_count = role_data.get('memberCount')

    async def update(self):
        """
        Updates information of the role.
        """
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
        """
        Edits the name, description or rank of a role

        Parameters
        ----------
        name : str, optional
            New name for the role.
        description : str, optional
            New description for the role.
        rank : int, optional
            Number from 1-254 that determains the new rank number for the role.

        Returns
        -------
        int
        """
        edit_req = await self.requests.patch(
            url=endpoint + f"/v1/groups/{self.group.id}/rolesets/{self.id}",
            data={
                "description": description if description else self.description,
                "name": name if name else self.name,
                "rank": rank if rank else self.rank
            }
        )
        return edit_req.status_code == 200

    async def edit_permissions(self, role_permissions):
        """
        Edits the permissions of a role.

        Parameters
        ----------
        role_permissions : ro_py.roles.RolePermissions
            New permissions that will overwrite the old ones.

        Returns
        -------
        int
        """
        data = {
            "permissions": {}
        }

        for key, value in get_rp_names(role_permissions):
            if value is True or False:
                data['permissions'][key] = value

        edit_req = await self.requests.patch(
            url=endpoint + f"/v1/groups/{self.group.id}/roles/{self.id}/permissions",
            data=data
        )

        return edit_req.status_code == 200
