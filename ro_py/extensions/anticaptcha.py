from ro_py.utilities.errors import IncorrectKeyError, InsufficientCreditError, NoAvailableWorkersError
from ro_py.captcha import UnsolvedCaptcha
import requests_async
import asyncio

endpoint = "https://2captcha.com"


class Task:
    def __init__(self):
        self.type = "FunCaptchaTaskProxyless"
        self.website_url = None
        self.website_public_key = None
        self.funcaptcha_api_js_subdomain = None

    def get_raw(self):
        return {
            "type": self.type,
            "websiteURL": self.website_url,
            "websitePublicKey": self.website_public_key,
            "funcaptchaApiJSSubdomain": self.funcaptcha_api_js_subdomain
        }


class AntiCaptcha:
    def __init__(self, api_key):
        self.api_key = api_key

    async def solve(self, captcha: UnsolvedCaptcha):
        task = Task()
        task.website_url = "https://roblox.com"
        task.website_public_key = captcha.pkey
        task.funcaptcha_api_js_subdomain = "https://roblox-api.arkoselabs.com"

        data = {
            "clientKey": self.api_key,
            "task": task.get_raw()
        }

        create_req = await requests_async.post('https://api.anti-captcha.com/createTask', json=data)
        create_res = create_req.json()
        if create_res['errorId'] == 1:
            raise IncorrectKeyError("The provided anit-captcha api key was incorrect.")
        if create_res['errorId'] == 2:
            raise NoAvailableWorkersError("There are currently no available workers.")
        if create_res['errorId'] == 10:
            raise InsufficientCreditError("Insufficient credit in the 2captcha account.")

        solution = None
        while True:
            await asyncio.sleep(5)
            check_data = {
                "clientKey": self.api_key,
                "taskId": create_res['taskId']
            }
            check_req = await requests_async.get("https://api.anti-captcha.com/getTaskResult", json=check_data)
            check_res = check_req.json()
            if check_res['status'] == "ready":
                solution = check_res['solution']['token']
                break

        return solution
