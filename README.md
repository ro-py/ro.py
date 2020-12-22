![Banner image for ro.py](https://raw.githubusercontent.com/jmk-developer/ro.py/main/resources/banner.svg)

# Welcome to ro.py
ro.py is a Python wrapper for the Roblox web API.
## Installation
You can install ro.py from pip:  
```
pip3 install ro-py
```
## Examples
Using the client:
```python
from ro_py.client import Client
client = Client("Token goes here")  # Token is optional, but allows for authentication!
```
Viewing a user's info:
```python
from ro_py.client import Client
client = Client()
user_id = 576059883
user = client.get_user(user_id)
print(f"Username: {user.name}")
print(f"Status: {user.get_status() or 'None.'}")
```
Find more examples in the examples folder.

## Credits
@mfd-co - helped with endpoints

## Other Libraries
https://github.com/RbxAPI/Pyblox  
https://github.com/iranathan/robloxapi  
