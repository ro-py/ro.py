"""

ro.py > asset_type.py

This file is a conversion table for asset type IDs to asset type names.

"""

from enum import IntEnum


class AssetTypes(IntEnum):
    Image = 1
    TeeShirt = 2
    Audio = 3
    Mesh = 4
    Lua = 5
    HTML = 6
    Text = 7
    Hat = 8
    Place = 9
    Model = 10

    Shirt = 11
    Pants = 12

    Decal = 13
    Avatar = 16
    Head = 17
    Face = 18
    Gear = 19
    Badge = 21
    GroupEmblem = 22
    Animation = 24

    Arms = 25
    Legs = 26
    Torso = 27
    RightArm = 28
    LeftArm = 29
    LeftLeg = 30
    RightLeg = 31
    Package = 32

    YouTubeVideo = 33
    GamePass = 34
    App = 45
    Code = 37
    Plugin = 38

    SolidModel = 39  # Fixed
    MeshPart = 40

    HairAccessory = 41
    FaceAccessory = 42
    NeckAccessory = 43
    ShoulderAccessory = 44
    FrontAccessory = 45
    BackAccessory = 46
    WaistAccessory = 47

    ClimbAnimation = 48
    DeathAnimation = 49
    FallAnimation = 50
    IdleAnimation = 51
    JumpAnimation = 52
    RunAnimation = 53
    SwimAniation = 54
    WalkAnimation = 55
    PoseAnimation = 56
    EarAccessory = 57
    EyeAccessory = 58

    LocalizationTableManifest = 59
    LocalizationTableTranslation = 60
    EmoteAnimation = 61
    Video = 62
    TexturePack = 63
