import requests
from urllib.parse import quote
import signalrcore.hub_connection_builder
from time import sleep


class NotificationReceiver:
    def __init__(self, rs):
        a = requests.get(
            url="https://realtime.roblox.com/notifications/negotiate?clientProtocol=1.5&connectionData=%5B%7B%22name"
                "%22%3A%22usernotificationhub%22%7D%5D",
            cookies={
                ".ROBLOSECURITY": rs
            }
        )

        print(a.text)

        final_url = f"wss://realtime.roblox.com/notifications?transport=websockets" \
                    f"&connectionToken={quote(a.json()['ConnectionToken'])}" \
                    f"&clientProtocol=1.5&connectionData=%5B%7B%22name%22%3A%22usernotificationhub%22%7D%5D"

        print(final_url)

        hub_connection = signalrcore.hub_connection_builder.HubConnectionBuilder()

        hub_connection.with_url(
            final_url,
            options={
                "headers": {
                    "Cookie": f".ROBLOSECURITY={rs}"
                }
            }
        )

        hub_connection.with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

        hub_connection.on_open(lambda d: print(d))
        hub_connection.on_close(lambda d: print(d))
        hub_connection.on("usernotificationhub", lambda: print("got thing"))
        hub_connection.start()

        while True:
            sleep(1 / 60)
