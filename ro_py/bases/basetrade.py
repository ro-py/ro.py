from ro_py.assets import Asset
import iso8601

from ro_py.utilities.url import url
endpoint = url("trades")


class PartialTrade:
    def __init__(self, cso, data):
        from ro_py.bases.baseuser import PartialUser
        self.cso = cso
        self.requests = cso.requests
        self.trade_id = data['id']
        self.user = PartialUser(cso, data['user'])
        self.created = iso8601.parse_date(data['created'])
        self.expiration = None
        if "expiration" in data:
            self.expiration = iso8601.parse_date(data['expiration'])
        self.status = data['status']

    async def accept(self) -> bool:
        """
        accepts a trade requests
        :returns: true/false
        """
        accept_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/accept"
        )
        return accept_req.status_code == 200

    async def decline(self) -> bool:
        """
        decline a trade requests
        :returns: true/false
        """
        decline_req = await self.requests.post(
            url=endpoint + f"/v1/trades/{self.trade_id}/decline"
        )
        return decline_req.status_code == 200

    async def expand(self):
        """
        Gets a more detailed trade request

        Returns
        -------
        ro_py.trades.Trade
        """

        from ro_py.trades import Trade
        expend_req = await self.requests.get(
            url=endpoint + f"/v1/trades/{self.trade_id}"
        )
        data = expend_req.json()

        # generate a user class and update it
        sender = await self.cso.client.get_user(data['user']['id'])
        await sender.update()

        # load items that will be/have been sent and items that you will/have receive(d)
        receive_items, send_items = [], []
        for items_0 in data['offers'][0]['userAssets']:
            item_0 = Asset(self.cso, items_0['assetId'])
            await item_0.update()
            receive_items.append(item_0)

        for items_1 in data['offers'][1]['userAssets']:
            item_1 = Asset(self.cso, items_1['assetId'])
            await item_1.update()
            send_items.append(item_1)

        return Trade(
            self.cso,
            data,
            sender,
            send_items,
            receive_items
        )
