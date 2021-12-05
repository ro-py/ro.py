"""

Contains classes and functions related to the authenticated Roblox account.
Not to be confused with users.py or the Account system.

"""

from datetime import date

from .utilities.shared import ClientSharedObject


class AccountProvider:
    """
    Provides methods that control the authenticated user's account.
    """

    def __init__(self, shared: ClientSharedObject):
        """
        Arguments:
            shared: The ClientSharedObject to be used when getting information on an account.
        """
        self._shared: ClientSharedObject = shared

    async def get_birthday(self) -> date:
        """
        Gets the authenticated user's birthday.
s
        Returns: 
            The authenticated user's birthday.
        """
        birthday_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("accountinformation", "v1/birthdate")
        )
        birthday_data = birthday_response.json()
        return date(
            month=birthday_data["birthMonth"],
            day=birthday_data["birthDay"],
            year=birthday_data["birthYear"]
        )

    async def set_birthday(
            self,
            birthday: date,
            password: str = None
    ):
        """
        Changes the authenticated user's birthday.
        This endpoint *may* require your password, and requires an unlocked PIN.

        Arguments:
            birthday: A date object that represents the birthay to update the ClientSharedObject's account to.
            password: The password to the ClientSharedObject's account, this is required when changing the birthday.
        """
        await self._shared.requests.post(
            url=self._shared.url_generator.get_url("accountinformation", "v1/birthdate"),
            json={
                "birthMonth": birthday.month,
                "birthDay": birthday.day,
                "birthYear": birthday.year,
                "password": password
            }
        )
