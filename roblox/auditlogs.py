from __future__ import annotations
from datetime import datetime
from enum import Enum
from dateutil.parser import parse
from roblox.members import Member
from roblox.partials.partialrole import PartialRole
from roblox.partials.partialuser import PartialUser
from roblox.utilities.shared import ClientSharedObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from roblox.groups import Group


class Actions(Enum):
    delete_post = "DeletePost"
    remove_member = "RemoveMember"
    accept_join_request = "AcceptJoinRequest"
    decline_join_request = "DeclineJoinRequest"
    post_shout = "PostStatus"
    change_rank = "ChangeRank"
    buy_ad = "BuyAd"
    send_ally_request = "SendAllyRequest"
    create_enemy = "CreateEnemy"
    accept_ally_request = "AcceptAllyRequest"
    decline_ally_request = "DeclineAllyRequest"
    delete_ally = "DeleteAlly"
    delete_enemy = "DeleteEnemy"
    add_group_place = "AddGroupPlace"
    remove_group_place = "RemoveGroupPlace"
    create_items = "CreateItems"
    configure_items = "ConfigureItems"
    spend_group_funds = "SpendGroupFunds"
    change_owner = "ChangeOwner"
    delete = "Delete"
    adjust_currency_amounts = "AdjustCurrencyAmounts"
    abandon = "Abandon"
    claim = "Claim"
    rename = "Rename"
    change_description = "ChangeDescription"
    invite_to_clan = "InviteToClan"
    cancel_clan_invite = "CancelClanInvite"
    kick_from_clan = "KickFromClan"
    buy_clan = "BuyClan"
    create_group_asset = "CreateGroupAsset"
    update_group_asset = "UpdateGroupAsset"
    configure_group_asset = "ConfigureGroupAsset"
    revert_group_asset = "RevertGroupAsset"
    create_group_developer_product = "CreateGroupDeveloperProduct"
    configure_group_game = "ConfigureGroupGame"
    lock = "Lock"
    unlock = "Unlock"
    create_game_pass = "CreateGamePass"
    create_badge = "CreateBadge"
    configure_badge = "ConfigureBadge"
    save_place = "SavePlace"
    publish_place = "PublishPlace"
    update_roleset_rank = "UpdateRolesetRank"
    update_roleset_data = "UpdateRolesetData"


class DeletePost:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action
        created: Datetime of creation of the audit_log
        target: The user who posted the post.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.target: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["TargetId"],
                                                                    "Name": data["description"]["TargetName"]})
        self.description: str = data["description"]["PostDesc"]


class RemoveMember:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action
        created: Datetime of creation of the audit_log
        target: User that was removed.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.target: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["TargetId"],
                                                                    "Name": data["description"]["TargetName"]})


class AcceptJoinRequest:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action
        created: Datetime of creation of the audit_log
        target: User who send the join request.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.target: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["TargetId"],
                                                                    "Name": data["description"]["TargetName"]})


class DeclineJoinRequest:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action
        created: Datetime of creation of the audit_log
        target: User who send the join request.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.target: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["TargetId"],
                                                                    "Name": data["description"]["TargetName"]})


class PostStatus:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action
        created: Datetime of creation of the audit_log
        text: text
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.text: str = data["description"]["Text"]


class ChangeRank:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User whose role was changed.
        new_role: New role the user got.
        old_role: Old role of the user.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: PartialUser = PartialUser(shared=shared, data={"id": data["description"]["TargetId"],
                                                                    "name": data["description"]["TargetName"]})
        self.new_role: PartialRole = PartialRole(shared=shared, data={"id": data["description"]["NewRoleSetId"],
                                                                      "name": data["description"]["NewRoleSetName"]})
        self.old_role: PartialRole = PartialRole(shared=shared, data={"id": data["description"]["OldRoleSetId"],
                                                                      "name": data["description"]["OldRoleSetName"]})


class BuyAd:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User that was removed.
        name: Name of the ad
        bid: how much you bid
        currency_type_id: type of currency id.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.name: str = data["description"]["AdName"]
        self.bid: int = data["description"]["Bid"]
        self.currency_type_id: int = data["description"]["CurrencyTypeId"]
        # CurrencyTypeName is always an emty string


class SendAllyRequest:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User that was removed.
        group:  The group that you send an ally request to.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})


class CreateEnemy:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User that was removed.
        group:  The group that you made your enemy.
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})


class AcceptAllyRequest:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User that was removed.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})


class DeclineAllyRequest:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: User that was removed.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})


class DeleteAlly:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: Group
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})


class DeleteEnemy:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        target: Group
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialgroup import UniversePartialGroup
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: UniversePartialGroup = UniversePartialGroup(shared=shared,
                                                                 data={"id": data["description"]["TargetGroupId"],
                                                                       "name": data["description"]["TargetGroupName"]})

class CreateItems:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        from roblox.partials.partialasset import PartialAsset
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.asset: PartialAsset = PartialAsset(shared=shared, data=data["description"])


class SpendGroupFunds:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.amount: int = data["description"]["Amount"]
        self.currency_type_id: int = data["description"]["CurrencyTypeId"]
        self.item_description: int = data["description"]["CurrencyTypeId"]


class ChangeOwner:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.is_roblox: int = data["description"]["IsRoblox"]
        self.old_owner: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["OldOwnerId"],
                                                                       "Name": data["description"]["OldOwnerName"]})
        self.new_owner: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["NewOwnerId"],
                                                                       "Name": data["description"]["NewOwnerName"]})


class ChangeDescription:
    """
    Represents a badge from the API.

    Attributes:
        actor: Member who did it.
        action_type: Type of the action.
        created: Datetime of creation of the audit_log.
        group:  The group that send you an ally request
    """

    def __init__(self, shared: ClientSharedObject, data: dict, group: Group):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on badges.
            data: The data from the endpoint.
            group: the group you have the audit logs from
        """
        self.shared: ClientSharedObject = shared
        self.group: Group = group
        self.actor: Member = Member(shared=self.shared, data=data["actor"], group=self.group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.new_description = data["description"]["NewDescription"]
