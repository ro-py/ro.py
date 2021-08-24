from __future__ import annotations

from datetime import datetime
from enum import Enum

from typing import Optional
import iso8601

from .bases.basegroup import BaseGroup
from .member import Member
from .partials.partialuser import PartialUser
from .role import Role
from .utilities.shared import ClientSharedObject


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


class Action:
    def __init__(self, shared: ClientSharedObject,
                 group: BaseGroup, raw_data: dict):
        self._shared: ClientSharedObject = shared
        self.group: BaseGroup = group

        actor_user = PartialUser(self._shared, raw_data["actor"]["user"])
        actor_role = Role(self._shared, self.group, raw_data["actor"]["role"])
        self.actor: Member =Member(self._shared, actor_user, self.group, actor_role)
        self.action: str = raw_data['actionType']
        self.created: datetime = iso8601.parse_date(raw_data['created'])
        self.data:  dict = raw_data['description']