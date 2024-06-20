import pytest
import json
from dateutil.parser import parse
from roblox import BaseUniverse, BaseAsset, Client
from roblox.assets import AssetType, asset_type_names
from roblox.badges import BadgeStatistics
from roblox.creatortype import CreatorType
from roblox.partials.partialgroup import UniversePartialGroup, AssetPartialGroup
from roblox.partials.partialuniverse import PartialUniverse
from roblox.partials.partialuser import PartialUser
from roblox.shout import Shout
from roblox.universes import UniverseGenre, UniverseAvatarType
from roblox.utilities.exceptions import UserNotFound, GroupNotFound, PlaceNotFound, UniverseNotFound, AssetNotFound, \
    PluginNotFound, BadgeNotFound
from roblox.bases.baseplace import BasePlace


def test_set_token():
    client = Client("Token")
    assert client._requests.session.cookies[".ROBLOSECURITY"] == "Token"


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [
    1,
    2,
    3,
    968108160,
    33655127,
])
async def test_get_user(client, user_id, vcr_cassette, event_loop):
    user = await client.get_user(user_id)
    data = json.loads(vcr_cassette.responses[0]["content"])
    assert data["description"] == user.description
    assert data["name"] == user.name
    assert data["displayName"] == user.display_name
    assert data["id"] == user.id
    assert data["externalAppDisplayName"] == user.external_app_display_name
    assert data["isBanned"] == user.is_banned
    assert parse(data["created"]) == user.created
    assert user.id == user_id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_id", [
    4,
    5
])
async def test_invalid_get_user(client, user_id):
    with pytest.raises(UserNotFound):
        await client.get_user(user_id)


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_get_authenticated_user(client, vcr_cassette):
    user = await client.get_authenticated_user(expand=False)
    data = json.loads(vcr_cassette.responses[0]["content"])
    assert data["name"] == user.name
    assert data["displayName"] == user.display_name
    assert data["id"] == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_expend_get_authenticated_user(client, vcr_cassette):
    user = await client.get_authenticated_user(expand=True)
    data = json.loads(vcr_cassette.responses[1]["content"])
    assert data["description"] == user.description
    assert data["name"] == user.name
    assert data["displayName"] == user.display_name
    assert data["id"] == user.id
    assert data["externalAppDisplayName"] == user.external_app_display_name
    assert data["isBanned"] == user.is_banned
    assert parse(data["created"]) == user.created


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_ids", [
    [2067807455, 1],
    [117091179, 2, 3],
])
async def test_get_users(client, user_ids, vcr_cassette):
    users = await client.get_users(user_ids)
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users_data) == len(users)
    for i in range(len(users)):
        data = users_data[i]
        user = users[i]
        assert data["displayName"] == user.display_name
        assert data["name"] == user.name
        assert data["id"] == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_ids", [
    [2067807455, 1],
    [117091179, 2, 3],
])
async def test_expand_get_users(client, user_ids, vcr_cassette):
    users = await client.get_users(user_ids, expand=True)
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users_data) == len(users)
    for i in range(len(users)):
        data = json.loads(vcr_cassette.responses[i + 1]["content"])
        data2 = users_data[i]
        user = users[i]

        assert data["description"] == user.description
        assert data["name"] == user.name
        assert data["displayName"] == user.display_name
        assert data["id"] == user.id
        assert data["externalAppDisplayName"] == user.external_app_display_name
        assert data["isBanned"] == user.is_banned
        assert parse(data["created"]) == user.created

        assert data2["displayName"] == user.display_name
        assert data2["name"] == user.name
        assert data2["id"] == user.id

        assert data2["displayName"] == data["displayName"]
        assert data2["name"] == data["name"]
        assert data2["id"] == data["id"]


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_banned_get_users(client, vcr_cassette):
    users = await client.get_users([39718632])
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users) == 1
    for i in range(len(users)):
        data = users_data[i]
        user = users[i]
        assert data["displayName"] == user.display_name
        assert data["name"] == user.name
        assert data["id"] == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_ids", [
    [39718632],
])
async def test_exclude_banned_users_true_get_users(client, user_ids):
    users = await client.get_users(user_ids, exclude_banned_users=True)
    assert len(users) == 0


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_name", [
    ["Boegie19", "local_ip"],
    ["Roblox", "John Doe", "Jane Doe"],
])
async def test_get_users_by_usernames(client, user_name, vcr_cassette):
    users = await client.get_users_by_usernames(user_name)
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users_data) == len(users)
    for i in range(len(users)):
        data = users_data[i]
        user = users[i]
        assert data["displayName"] == user.display_name
        assert data["name"] == user.name
        assert data["id"] == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_name", [
    "Roblox",
    "John Doe",
    "Jane Doe",
    "local_ip",
    "Boegie19",
])
async def test_get_user_by_username(event_loop, client, user_name, vcr_cassette):
    user = await client.get_user_by_username(user_name)
    data = json.loads(vcr_cassette.responses[0]["content"])["data"][0]
    assert data["name"] == user.name
    assert data["displayName"] == user.display_name
    assert data["id"] == user.id
    assert user.name == user_name


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_name", [
    "Roblox",
    "John Doe",
    "Jane Doe",
    "local_ip",
    "Boegie19",
])
async def test_expend_get_user_by_username(client, user_name, vcr_cassette):
    user = await client.get_user_by_username(user_name, expand=True)
    data = json.loads(vcr_cassette.responses[1]["content"])
    assert data["description"] == user.description
    assert data["name"] == user.name
    assert data["displayName"] == user.display_name
    assert data["id"] == user.id
    assert data["externalAppDisplayName"] == user.external_app_display_name
    assert data["isBanned"] == user.is_banned
    assert parse(data["created"]) == user.created
    assert user.name == user_name


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_name", [
    ["ErichModel"],
])
async def test_banned_get_users_by_username(client, user_name, vcr_cassette):
    users = await client.get_users_by_usernames(user_name)
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users) == 1
    for i in range(len(users)):
        data = users_data[i]
        user = users[i]
        assert data["displayName"] == user.display_name
        assert data["name"] == user.name
        assert data["id"] == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("user_name", [
    "ErichModel",
])
async def test_invalid_exclude_banned_users_true_get_users__by_username(client, user_name):
    with pytest.raises(UserNotFound):
        await client.get_user_by_username(user_name, exclude_banned_users=True, expand=True)


@pytest.mark.parametrize("user_id", [
    1,
    117091179,
])
def test_get_base_user(client, user_id):
    user = client.get_base_user(user_id)
    assert user_id == user.id


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_user_search(client, vcr_cassette):
    object = client.user_search("123")
    users = await object.next()
    users_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(users_data) == len(users)
    for i in range(len(users)):
        data = users_data[i]
        user = users[i]
        assert data["displayName"] == user.display_name
        assert data["name"] == user.name
        assert data["id"] == user.id
        assert data["previousUsernames"] == user.previous_usernames


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("group_id", [
    9695397,
    10720185,
])
async def test_get_group(client, group_id, vcr_cassette):
    group = await client.get_group(group_id)
    data = json.loads(vcr_cassette.responses[0]["content"])
    assert group.id == data["id"]
    assert group.name == data["name"]
    assert group.description == data["description"]

    assert type(group.owner) == PartialUser or type(group.owner) is None
    if type(group.owner) == PartialUser:
        assert group.owner.id == data["owner"]["userId"]
        assert group.owner.name == data["owner"]["username"]
        assert group.owner.display_name == data["owner"]["displayName"]

    assert type(group.shout) == Shout or type(group.shout) is None
    if type(group.shout) == Shout:
        group.shout.body = data["shout"]["body"]

        assert type(group.shout.poster) == PartialUser
        assert group.shout.poster.id == data["shout"]["poster"]["userId"]
        assert group.shout.poster.name == data["shout"]["poster"]["username"]
        assert group.shout.poster.display_name == data["shout"]["poster"]["displayName"]

        assert group.shout.created == parse(data["shout"]["created"])
        assert group.shout.updated == parse(data["shout"]["updated"])

    assert group.member_count == data["memberCount"]
    assert group.is_builders_club_only == data["isBuildersClubOnly"]
    assert group.public_entry_allowed == data["publicEntryAllowed"]
    assert group.is_locked == data.get("isLocked") or group.is_locked is False


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("group_id", [
    12
])
async def test_invalid_get_group(client, group_id):
    with pytest.raises(GroupNotFound):
        await client.get_group(group_id)


@pytest.mark.parametrize("group_id", [
    9695397,
    10720185,
])
def test_get_base_group(client, group_id):
    group = client.get_base_group(group_id)
    assert group_id == group.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("universe_ids", [
    [679715583, 2042724756],
])
async def test_get_universes(client, universe_ids, vcr_cassette):
    universes = await client.get_universes(universe_ids)
    universes_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(universes_data) == len(universes)
    for i in range(len(universe_ids)):
        universe = universes[i]
        data = universes_data[i]
        assert universe.id == data["id"]
        assert universe.name == data["name"]
        assert universe.description == data["description"]
        assert universe.price == data["price"]
        assert universe.allowed_gear_genres == data["allowedGearGenres"]
        assert universe.allowed_gear_categories == data["allowedGearCategories"]
        assert universe.is_genre_enforced == data["isGenreEnforced"]
        assert universe.copying_allowed == data["copyingAllowed"]
        assert universe.playing == data["playing"]
        assert universe.visits == data["visits"]
        assert universe.max_players == data["maxPlayers"]
        assert universe.created == parse(data["created"])
        assert universe.updated == parse(data["updated"])
        assert universe.studio_access_to_apis_allowed == data["studioAccessToApisAllowed"]
        assert universe.create_vip_servers_allowed == data["createVipServersAllowed"]
        assert universe.is_all_genre == data["isAllGenre"]
        # gameRating seems to be null across all games, so I omitted it from this class.
        assert universe.is_favorited_by_user == data["isFavoritedByUser"]
        assert universe.favorited_count == data["favoritedCount"]
        assert type(universe.root_place) == BasePlace
        assert universe.root_place.id == data["rootPlaceId"]
        assert universe.creator_type == CreatorType(data["creator"]["type"])
        assert universe.genre == UniverseGenre(data["genre"])
        assert universe.universe_avatar_type == UniverseAvatarType(data["universeAvatarType"])
        if universe.creator_type == CreatorType.group:
            assert type(universe.creator) == UniversePartialGroup
            assert universe.creator.id == data["creator"]["id"]
            assert universe.creator.name == data["creator"]["name"]
        elif universe.creator_type == CreatorType.user:
            assert type(universe.creator) == PartialUser
            assert universe.creator.id == data["creator"]["id"]
            assert universe.creator.name == data["creator"]["name"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("universe_id", [
    2042724756,
])
async def test_get_universe(client, universe_id, vcr_cassette):
    universes = await client.get_universe(universe_id)
    universes_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    universe = universes
    data = universes_data[0]
    assert universe.id == data["id"]
    assert universe.name == data["name"]
    assert universe.description == data["description"]
    assert universe.price == data["price"]
    assert universe.allowed_gear_genres == data["allowedGearGenres"]
    assert universe.allowed_gear_categories == data["allowedGearCategories"]
    assert universe.is_genre_enforced == data["isGenreEnforced"]
    assert universe.copying_allowed == data["copyingAllowed"]
    assert universe.playing == data["playing"]
    assert universe.visits == data["visits"]
    assert universe.max_players == data["maxPlayers"]
    assert universe.created == parse(data["created"])
    assert universe.updated == parse(data["updated"])
    assert universe.studio_access_to_apis_allowed == data["studioAccessToApisAllowed"]
    assert universe.create_vip_servers_allowed == data["createVipServersAllowed"]
    assert universe.is_all_genre == data["isAllGenre"]
    # gameRating seems to be null across all games, so I omitted it from this class.
    assert universe.is_favorited_by_user == data["isFavoritedByUser"]
    assert universe.favorited_count == data["favoritedCount"]
    assert type(universe.root_place) == BasePlace
    assert universe.root_place.id == data["rootPlaceId"]
    assert universe.creator_type == CreatorType(data["creator"]["type"])
    assert universe.genre == UniverseGenre(data["genre"])
    assert universe.universe_avatar_type == UniverseAvatarType(data["universeAvatarType"])
    if universe.creator_type == CreatorType.group:
        assert type(universe.creator) == UniversePartialGroup
        assert universe.creator.id == data["creator"]["id"]
        assert universe.creator.name == data["creator"]["name"]
    elif universe.creator_type == CreatorType.user:
        assert type(universe.creator) == PartialUser
        assert universe.creator.id == data["creator"]["id"]
        assert universe.creator.name == data["creator"]["name"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("universe_id", [
    0,
])
async def test_invalid_get_universe(client, universe_id):
    with pytest.raises(UniverseNotFound):
        await client.get_universe(universe_id)


@pytest.mark.parametrize("universe_id", [
    0,
    1,
])
def test_get_base_universe(client, universe_id):
    universe = client.get_base_universe(universe_id)
    assert universe_id == universe.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("place_ids", [
    [5759259638, 2677609345]
])
async def test_get_places(client, place_ids, vcr_cassette):
    places = await client.get_places(place_ids)
    places_data = json.loads(vcr_cassette.responses[0]["content"])
    assert len(places_data) == len(places)
    for i in range(len(place_ids)):
        place = places[i]
        data = places_data[i]
        assert place.id == data["placeId"]
        assert place.name == data["name"]
        assert place.description == data["description"]
        assert place.url == data["url"]

        assert place.builder == data["builder"]
        assert place.builder_id == data["builderId"]

        assert place.is_playable == data["isPlayable"]
        assert place.reason_prohibited == data["reasonProhibited"]

        assert type(place.universe) == BaseUniverse
        assert place.universe.id == data["universeId"]

        assert type(place.universe_root_place) == BasePlace
        assert place.universe_root_place.id == data["universeRootPlaceId"]

        assert place.price == data["price"]
        assert place.image_token == data["imageToken"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("place_id", [
    5759259638, 2677609345
])
async def test_get_place(client, place_id, vcr_cassette):
    place = await client.get_place(place_id)
    data = json.loads(vcr_cassette.responses[0]["content"])[0]
    assert place.id == data["placeId"]
    assert place.name == data["name"]
    assert place.description == data["description"]
    assert place.url == data["url"]

    assert place.builder == data["builder"]
    assert place.builder_id == data["builderId"]

    assert place.is_playable == data["isPlayable"]
    assert place.reason_prohibited == data["reasonProhibited"]

    assert type(place.universe) == BaseUniverse
    assert place.universe.id == data["universeId"]

    assert type(place.universe_root_place) == BasePlace
    assert place.universe_root_place.id == data["universeRootPlaceId"]

    assert place.price == data["price"]
    assert place.image_token == data["imageToken"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("place_id", [
    0
])
async def test_invalid_get_place(client, place_id):
    with pytest.raises(PlaceNotFound):
        await client.get_place(place_id)


@pytest.mark.parametrize("place_id", [
    0,
    1,
])
def test_get_base_place(client, place_id):
    asset = client.get_base_place(place_id)
    assert place_id == asset.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("asset_id", [
    20372960
])
async def test_get_asset(client, asset_id, vcr_cassette):
    asset = await client.get_asset(asset_id)
    data = json.loads(vcr_cassette.responses[0]["content"])

    assert asset.product_type == data["ProductType"]
    assert asset.id == data["AssetId"]
    assert asset.product_id == data["ProductId"]
    assert asset.name == data["Name"]
    assert asset.description == data["Description"]

    assert type(asset.type) == AssetType
    assert asset.type.id == data["AssetTypeId"]
    assert asset.type.name == asset_type_names.get(data["AssetTypeId"])

    assert asset.creator_type == CreatorType(data["Creator"]["CreatorType"])

    if asset.creator_type == CreatorType.user:
        assert type(asset.creator) == PartialUser
    elif asset.creator_type == CreatorType.group:
        assert type(asset.creator) == AssetPartialGroup

    assert type(asset.icon_image) == BaseAsset
    assert asset.icon_image.id == data["IconImageAssetId"]

    assert asset.created == parse(data["Created"])
    assert asset.updated == parse(data["Updated"])

    assert asset.price == data["PriceInRobux"]
    assert asset.sales == data["Sales"]

    assert asset.is_new == data["IsNew"]
    assert asset.is_for_sale == data["IsForSale"]
    assert asset.is_public_domain == data["IsPublicDomain"]
    assert asset.is_limited == data["IsLimited"]
    assert asset.is_limited_unique == data["IsLimitedUnique"]

    assert asset.remaining == data["Remaining"]

    assert asset.minimum_membership_level == data["MinimumMembershipLevel"]
    assert asset.content_rating_type_id == data["ContentRatingTypeId"]
    assert asset.sale_availability_locations == data["SaleAvailabilityLocations"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("asset_id", [
    0
])
async def test_invalid_get_asset(client, asset_id):
    with pytest.raises(AssetNotFound):
        await client.get_asset(asset_id)


@pytest.mark.parametrize("asset_id", [
    0,
    1,
])
def test_get_base_asset(client, asset_id):
    asset = client.get_base_asset(asset_id)
    assert asset_id == asset.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("plugin_ids", [
    [948084095, 4749111907]
])
async def test_get_plugins(client, plugin_ids, vcr_cassette):
    plugins = await client.get_plugins(plugin_ids)
    plugins_data = json.loads(vcr_cassette.responses[0]["content"])["data"]
    assert len(plugins) == len(plugins_data)
    for i in range(len(plugins)):
        plugin = plugins[i]
        data = plugins_data[i]
        assert plugin.id == data["id"]
        assert plugin.name == data["name"]
        assert plugin.description == data["description"]
        assert plugin.comments_enabled == data["commentsEnabled"]
        assert plugin.version_id == data["versionId"]
        assert plugin.created == parse(data["created"])
        assert plugin.updated == parse(data["updated"])


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("plugin_id", [
    948084095, 4749111907
])
async def test_get_plugin(client, plugin_id, vcr_cassette):
    plugin = await client.get_plugin(plugin_id)
    data = json.loads(vcr_cassette.responses[0]["content"])["data"][0]
    assert plugin.id == data["id"]
    assert plugin.name == data["name"]
    assert plugin.description == data["description"]
    assert plugin.comments_enabled == data["commentsEnabled"]
    assert plugin.version_id == data["versionId"]
    assert plugin.created == parse(data["created"])
    assert plugin.updated == parse(data["updated"])


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("plugin_id", [
    0
])
async def test_invalid_get_plugin(client, plugin_id):
    with pytest.raises(PluginNotFound):
        await client.get_plugin(plugin_id)


@pytest.mark.parametrize("plugin_id", [
    0,
    1,
])
def test_get_base_plugin(plugin_id, client):
    plugin = client.get_base_plugin(plugin_id)
    assert plugin_id == plugin.id


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("badge_id", [
    2124467043
])
async def test_get_badge(client, badge_id, vcr_cassette):
    badge = await client.get_badge(badge_id)
    data = json.loads(vcr_cassette.responses[0]["content"])
    assert badge.name == data["name"]
    assert badge.description == data["description"]
    assert badge.display_name == data["displayName"]
    assert badge.display_description == data["displayDescription"]
    assert badge.enabled == data["enabled"]
    assert type(badge.icon) == BaseAsset
    assert badge.icon.id == data["iconImageId"]

    assert type(badge.display_icon) == BaseAsset
    assert badge.display_icon.id == data["displayIconImageId"]

    assert badge.created == parse(data["created"])
    assert badge.updated == parse(data["updated"])

    assert type(badge.statistics) == BadgeStatistics
    assert badge.statistics.past_day_awarded_count == data["statistics"]["pastDayAwardedCount"]
    assert badge.statistics.awarded_count == data["statistics"]["awardedCount"]
    assert badge.statistics.win_rate_percentage == data["statistics"]["winRatePercentage"]

    assert type(badge.awarding_universe) == PartialUniverse
    assert badge.awarding_universe.id == data["awardingUniverse"]["id"]
    assert badge.awarding_universe.name == data["awardingUniverse"]["name"]
    assert badge.awarding_universe.id == data["awardingUniverse"]["id"]

    assert type(badge.awarding_universe.root_place) == BasePlace
    assert badge.awarding_universe.root_place.id == data["awardingUniverse"]["rootPlaceId"]


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.parametrize("badge_id", [
    0
])
async def test_invalid_get_badge(client, badge_id):
    with pytest.raises(BadgeNotFound):
        await client.get_badge(badge_id)


@pytest.mark.parametrize("badge_id", [
    0,
    1,
])
def test_get_base_badge(client, badge_id):
    badge = client.get_base_badge(badge_id)
    assert badge_id == badge.id


@pytest.mark.parametrize("gamepass_id", [
    0,
    1,
])
def test_get_base_gamepass(client, gamepass_id):
    gamepass = client.get_base_gamepass(gamepass_id)
    assert gamepass_id == gamepass.id