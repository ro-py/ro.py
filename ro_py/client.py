from ro_py.users import User
from ro_py.groups import Group
from ro_py.utilities.requests import Requests
from ro_py.accountinformation import AccountInformation


class Client:
    def __init__(self, token=None):
        self.token = token
        self.requests = Requests()
        if token:
            self.requests.cookies[".ROBLOSECURITY"] = token
        self.accountinformation = AccountInformation(self.requests)
        self.requests.update_xsrf()

    def get_user(self, user_identifier):
        return User(self.requests, user_identifier)

    def get_group(self, group_id):
        return Group(self.requests, group_id)
