"""

ro.py > accountinformation.py

This file houses functions and classes that pertain to Roblox client .

"""

from datetime import datetime
from ro_py.gender import RobloxGender

endpoint = "https://accountinformation.roblox.com/"


class AccountInformationMetadata:
    """
    Represents account information metadata.
    """
    def __init__(self, metadata_raw):
        self.is_allowed_notifications_endpoint_disabled = metadata_raw["isAllowedNotificationsEndpointDisabled"]
        self.is_account_settings_policy_enabled = metadata_raw["isAccountSettingsPolicyEnabled"]
        self.is_phone_number_enabled = metadata_raw["isPhoneNumberEnabled"]
        self.max_user_description_length = metadata_raw["MaxUserDescriptionLength"]
        self.is_user_description_enabled = metadata_raw["isUserDescriptionEnabled"]
        self.is_user_block_endpoints_updated = metadata_raw["isUserBlockEndpointsUpdated"]


class PromotionChannels:
    """
    Represents account information promotion channels.
    """
    def __init__(self, promotion_raw):
        self.promotion_channels_visibility_privacy = promotion_raw["promotionChannelsVisibilityPrivacy"]
        self.facebook = promotion_raw["facebook"]
        self.twitter = promotion_raw["twitter"]
        self.youtube = promotion_raw["youtube"]
        self.twitch = promotion_raw["twitch"]


class AccountInformation:
    """
    Represents authenticated client account information (https://accountinformation.roblox.com/)
    This is only available for authenticated clients as it cannot be accessed otherwise.
    """
    def __init__(self, requests):
        self.requests = requests
        self.account_information_metadata = None
        self.promotion_channels = None
        self.update()

    def update(self):
        """
        Updates the account information.
        :return: Nothing
        """
        account_information_req = self.requests.get("https://accountinformation.roblox.com/v1/metadata")
        self.account_information_metadata = AccountInformationMetadata(account_information_req.json())
        promotion_channels_req = self.requests.get("https://accountinformation.roblox.com/v1/promotion-channels")
        self.promotion_channels = PromotionChannels(promotion_channels_req.json())

    def get_gender(self):
        """
        Returns the user's gender.
        :return: RobloxGender
        """
        gender_req = self.requests.get(endpoint + "v1/gender")
        return RobloxGender(gender_req.json()["gender"])

    def set_gender(self, gender):
        """
        Sets the user's gender.
        :param gender: RobloxGender
        :return: Nothing
        """
        gender_req = self.requests.post(
            url=endpoint + "v1/gender",
            data={
                "gender": str(gender.value)
            }
        )

    def get_birthdate(self):
        """
        Returns the user's birthdate.
        :return: datetime
        """
        birthdate_req = self.requests.get(endpoint + "v1/birthdate")
        birthdate_raw = birthdate_req.json()
        birthdate = datetime(
            year=birthdate_raw["birthYear"],
            month=birthdate_raw["birthMonth"],
            day=birthdate_raw["birthDay"]
        )
        return birthdate

    def set_birthdate(self, birthdate):
        """
        Sets the user's birthdate.
        :param birthdate: A datetime object.
        :return: Nothing
        """
        birthdate_req = self.requests.post(
            url=endpoint + "v1/birthdate",
            data={
              "birthMonth": birthdate.month,
              "birthDay": birthdate.day,
              "birthYear": birthdate.year
            }
        )
