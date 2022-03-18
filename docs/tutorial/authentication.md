# Authentication
To authenticate our client, we need our .ROBLOSECURITY token. To learn about why we need this and how to get it, 
please see [ROBLOSECURITY](/roblosecurity). 

Once we have our token, we can add it to our client by passing it as the first parameter. 
Use the following code and replace `TOKEN` with the .ROBLOSECURITY token grabbed earlier to authenticate your client.
```python
from roblox import Client
client = Client("TOKEN")
```

To test your token, replace the code in `main()` with the following:
```python
user = await client.get_authenticated_user()
print("ID:", user.id)
print("Name:", user.name)
```
If this raises an error, or the name and ID differ from what is expected, follow the instructions and try again.
The issue with this structure is that it is not secure. It's easy to slip up and copy your code and accidentally send 
someone your token, and it makes it harder to collaborate on code with others.

# Using a .env file
To solve this problem, we'll create a separate file called `.env` which will contain our token.  

Your file should look like this, where TOKEN is the .ROBLOSECURITY token you grabbed earlier.
```dotenv title=".env"
ROBLOXTOKEN=TOKEN
```
Place it in the same folder as your application's main file. 

Your file structure should look like this:
```sh
.
├─ .env
└─ main.py
```

Next, install the [python-dotenv](https://github.com/theskumar/python-dotenv) library with the following command:
```
$ pip install python-dotenv
```
Then, add these lines to the top of your code:
```python
import os
from dotenv import load_dotenv
```
After that, replace the code where you generate your client with this:
```python
load_dotenv()
client = Client(os.getenv("ROBLOXTOKEN"))
```
Test it with `get_authenticated_user` and you should be all set!
!!! abstract "Finished code"
    ```python title="main.py"
    import asyncio
    import os
    from dotenv import load_dotenv
    from roblox import Client
    
    load_dotenv()

    client = Client(os.getenv("ROBLOXTOKEN"))
    
    async def main():
        user = await client.get_authenticated_user()
        print("ID:", user.id)
        print("Name:", user.name)
    
    asyncio.get_event_loop().run_until_complete(main())
    ```
