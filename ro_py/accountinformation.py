from datetime import datetime

endpoint = "https://accountinformation.roblox.com/"


class AccountInformationMetadata:
    def __init__(self):
        pass


class AccountInformation:
    def __init__(self, requests):
        self.requests = requests

    def get_gender(self):
        """
        Returns the user's gender.
        :return: An integer.
        """
        gender_req = self.requests.get(endpoint + "v1/birthdate")
        return gender_req.json()["gender"]

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
