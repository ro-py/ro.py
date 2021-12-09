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
    delete_post = "deletePost"
    remove_member = "removeMember"
    accept_join_request = "Accept Join Request"
    decline_join_request = "declineJoinRequest"
    post_shout = "postShout"
    change_rank = "Change Rank"
    buy_ad = "buyAd"
    send_ally_request = "sendAllyRequest"
    create_enemy = "createEnemy"
    accept_ally_request = "acceptAllyRequest"
    decline_ally_request = "declineAllyRequest"
    delete_ally = "deleteAlly"
    add_group_place = "addGroupPlace"
    delete_group_place = "deleteGroupPlace"
    create_items = "createItems"
    configure_items = "configureItems"
    spend_group_funds = "spendGroupFunds"
    change_owner = "changeOwner"
    delete = "delete"
    adjust_currency_amounts = "adjustCurrencyAmounts"
    abandon = "abandon"
    claim = "claim"
    rename = "rename"
    change_description = "changeDescription"
    create_group_asset = "createGroupAsset"
    upload_group_asset = "uploadGroupAsset"
    configure_group_asset = "configureGroupAsset"
    revert_group_asset = "revertGroupAsset"
    create_group_developer_product = "createGroupDeveloperProduct"
    configure_group_game = "configureGroupGame"
    lock = "lock"
    unlock = "unlock"
    create_game_pass = "createGamePass"
    create_badge = "createBadge"
    configure_badge = "configureBadge"
    save_place = "savePlace"
    publish_place = "publishPlace"
    invite_to_clan = "inviteToClan"
    kick_from_clan = "kickFromClan"
    cancel_clan_invite = "cancelClanInvite"
    buy_clan = "buyClan"


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
        """
        self.actor: Member = Member(shared=shared, data=data["actor"], group=group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])

        self.target: PartialUser = PartialUser(shared=shared, data={"Id": data["description"]["TargetId"],
                                                                    "Name": data["description"]["TargetName"]})


class ChangeRank:
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
        """
        self.actor: Member = Member(shared=shared, data=data["actor"], group=group)
        self.action_type: str = data["actionType"]
        self.created: datetime = parse(data["created"])
        self.target: PartialUser = PartialUser(shared=shared, data={"id": data["description"]["TargetId"],
                                                                    "name": data["description"]["TargetName"]})
        self.new_role: PartialRole = PartialRole(shared=shared, data={"id": data["description"]["NewRoleSetId"],
                                                                      "name": data["description"]["NewRoleSetName"]})
        self.old_role: PartialRole = PartialRole(shared=shared, data={"id": data["description"]["OldRoleSetId"],
                                                                      "name": data["description"]["OldRoleSetName"]})
