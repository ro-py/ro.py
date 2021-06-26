from __future__ import annotations

from enum import Enum

import iso8601
import roblox.user
import roblox.role
import roblox.member
import roblox.bases.basegroup
import datetime
import roblox.utilities.clientshardobject


class Action:
    def __init__(self, cso: roblox.utilities.clientshardobject.ClientSharedObject,
                 group: roblox.bases.basegroup.BaseGroup, raw_data: dict):
        self.cso: roblox.utilities.clientshardobject.ClientSharedObject = cso
        self.group: roblox.bases.basegroup.BaseGroup = group

        actor_user = roblox.user.PartialUser(self.cso, raw_data["actor"]["user"])
        actor_role = roblox.role.Role(self.cso, self.group, raw_data["actor"]["role"])
        self.actor: roblox.member.Member = roblox.member.Member(self.cso, actor_user, self.group, actor_role)
        self.action: str = raw_data['actionType']
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        self.data: dict = raw_data['description']
        self.newdata: Description = Description.from_action(raw_data['actionType'], raw_data['description'])


class Description:

    def __init__(self, type, description):
        self.action: str = type

    @classmethod
    def from_action(cls, action, description) -> Description:
        for c in cls.__subclasses__():
            if ActionsToClasses[action]:
                break
        else:
            raise ValueError("Unknown type: {!r}".format(action))
        return c(action, description)


class DeletePost(Description):

    def __init__(self, action, description):
        super().__init__(action, description)


class RemoveMember(Description):
    def __init__(self, action, description):
        super().__init__(action, description)


class AcceptJoinRequest(Description):
    def __init__(self, action, description):
        super().__init__(action, description)


class ActionsToClasses(Enum):
    deletePost = DeletePost
    removeMember = RemoveMember
    accept_join_request = AcceptJoinRequest
    decline_join_request = "declineJoinRequest"
    post_shout = "postShout"
    change_rank = "changeRank"
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


class Actions(Enum):
    delete_post = "deletePost"
    remove_member = "removeMember"
    accept_join_request = "acceptJoinRequest"
    decline_join_request = "declineJoinRequest"
    post_shout = "postShout"
    change_rank = "changeRank"
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
