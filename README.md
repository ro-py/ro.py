# Welcome to ro.py
ro.py is a Python wrapper for the Roblox web API.
## Installation
You can install ro.py from pip:  
```
pip3 install ro-py
```
## Examples
Reading a user's description:  
```python
from ro_py import User
user = User(576059883)
print(f"Username: {user.name}")
print(f"Description: {user.description}")
```
Reading a game's votes:  
```python
from ro_py import Game
game = Game(1732173541)  # This takes in a Universe ID and not a Place ID
votes = game.get_votes()
print(f"Likes: {votes.up_votes}")
print(f"Dislikes: {votes.down_votes}")
```
You can read more examples in the `examples` directory.
## Other Libraries
https://github.com/RbxAPI/Pyblox  
https://github.com/iranathan/robloxapi  