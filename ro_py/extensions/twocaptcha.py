from ro_py.utilities.errors import IncorrectKeyError, InsufficientCreditError, NoAvailableWorkersError
from ro_py.captcha import UnsolvedCaptcha
import requests_async
import asyncio

endpoint = "https://2captcha.com"


class TwoCaptcha:
    # roblox-api.arkoselabs.com
    def __init__(self, api_key):
        self.api_key = api_key

    async def solve(self, captcha: UnsolvedCaptcha):
        url = endpoint + "/in.php"
        url += f"?key={self.api_key}"
        url += "&method=funcaptcha"
        url += f"&publickey={captcha.pkey}"
        url += "&surl=https://roblox-api.arkoselabs.com"
        url += "&pageurl=https://www.roblox.com"
        url += "&json=1"
        print(url)

        solve_req = await requests_async.post(url)
        print(solve_req.text)
        data = solve_req.json()
        if data['request'] == "ERROR_WRONG_USER_KEY" or data['request'] == "ERROR_KEY_DOES_NOT_EXIST":
            raise IncorrectKeyError("The provided 2captcha api key was incorrect.")
        if data['request'] == "ERROR_ZERO_BALANCE":
            raise InsufficientCreditError("Insufficient credit in the 2captcha account.")
        if data['request'] == "ERROR_NO_SLOT_AVAILABLE":
            raise NoAvailableWorkersError("There are currently no available workers.")
        task_id = data['request']

        solution = None
        while True:
            await asyncio.sleep(5)
            captcha_req = await requests_async.get(endpoint + f"/res.php"
                                                              f"?key={self.api_key}"
                                                              f"&id={task_id}"
                                                              f"&json=1&action=get")
            captcha_data = captcha_req.json()
            if captcha_data['request'] != "CAPCHA_NOT_READY":
                solution = captcha_data['request']
                break
        return solution
