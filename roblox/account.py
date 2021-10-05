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
        self._shared: ClientSharedObject = shared

    async def get_birthday(self) -> date:
        """
        Gets the authenticated user's birthday.
        Returns: The authenticated user's birthday.
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
        """
        self._shared.requests.post(
            url=self._shared.url_generator.get_url("accountinformation", "v1/birthdate"),
            json={
                "birthMonth": date.month,
                "birthDay": date.day,
                "birthYear": date.year,
                "password": password
            }
        )

