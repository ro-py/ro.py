from ro_py import Asset

asset_id = 130213380

print(f"Loading asset {asset_id}...")
asset = Asset(asset_id)
print("Loaded assset.")

print(f"Name: {asset.name}")
print(f"Description: {asset.description}")
print(f"Limited: {asset.is_limited}")
if asset.is_limited:
    resale_data = asset.limited_resale_data
    print(f"Original Price: {resale_data.original_price}")
    print(f"Number Remaining: {resale_data.number_remaining}")
    print(f"Recent Average Price: {resale_data.recent_average_price}")
    print(f"Stock: {resale_data.asset_stock}")
    print(f"Sales: {resale_data.sales}")
else:
    print(f"Price: {asset.price} R$")
print(f"Created: {asset.created.strftime('%b %d %Y %H:%M:%S')}")
print(f"Updated: {asset.updated.strftime('%b %d %Y %H:%M:%S')}")
