from __future__ import annotations

from enum import Enum

from typing import Optional
import iso8601
import roblox.user
import roblox.role
import roblox.member
import roblox.bases.basegroup
import datetime
import roblox.utilities.clientsharedobject


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


class Action:
    def __init__(self, cso: roblox.utilities.clientsharedobject.ClientSharedObject,
                 group: roblox.bases.basegroup.BaseGroup, raw_data: dict):
        self.cso: roblox.utilities.clientsharedobject.ClientSharedObject = cso
        self.group: roblox.bases.basegroup.BaseGroup = group

        actor_user = roblox.user.PartialUser(self.cso, raw_data["actor"]["user"])
        actor_role = roblox.role.Role(self.cso, self.group, raw_data["actor"]["role"])
        self.actor: roblox.member.Member = roblox.member.Member(self.cso, actor_user, self.group, actor_role)
        self.action: str = raw_data['actionType']
        self.created: datetime.datetime = iso8601.parse_date(raw_data['created'])
        self.data:  dict = raw_data['description']
        #self.data:  dict = Description.from_action(self.cso, raw_data['actionType'],raw_data['description'])


class Description:
    action = None

    def __init__(self, cso,description):
        self.cso = cso
        self.target: Optional[roblox.user.PartialUser]