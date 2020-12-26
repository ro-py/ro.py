from ro_py.client import Client

client = Client()

user_id = 576059883

print(f"Loading user {user_id}...")
user = client.get_user(user_id)
print("Loaded user.")

print(f"Username: {user.name}")
print(f"Display Name: {user.display_name}")
print(f"Description: {user.description}")
print(f"Status: {user.get_status() or 'None.'}")
