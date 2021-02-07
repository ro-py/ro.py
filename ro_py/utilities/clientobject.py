class ClientObject:
    """
    Every object that is grabbable with client.get_x inherits this object.
    """
    async def update(self):
        pass
