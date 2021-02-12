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
    Hat = 8
    Place = 9
    Model = 10

    Shirt = 11
    Pants = 12

    Decal = 13
    Head = 17
    Face = 18
    Gear = 19
    Badge = 21
    Animation = 24

    Torso = 27
    RightArm = 28
    LeftArm = 29
    LeftLeg = 30
    RightLeg = 31
    Package = 32

    GamePass = 34
    Plugin = 38
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

    EmoteAnimation = 61
    Video = 62
