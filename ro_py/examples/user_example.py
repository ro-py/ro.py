from ro_py import User

user_id = 576059883

print(f"Loading user {user_id}...")
user = User(user_id)
print("Loaded user.")

print(f"Username: {user.name}")
print(f"Display Name: {user.display_name}")
print(f"Description: {user.description}")
print(f"Status: {user.status}")
