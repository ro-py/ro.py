class BaseAsset:
    def __init__(self):
        self.id = None
        self.cso = None

    async def to_asset(self):
        return await self.cso.client.get_asset(self.id)
