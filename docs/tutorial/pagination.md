# Pagination
Certain Roblox endpoints are paginated. This means that going through their data is kind of like flipping through the
pages of a book - you start at page 1 and then you can move forwards or backwards until you reach the start or the end.

This can be annoying when all you want is "every member in a group" or "the last 10 posts on a group wall", so ro.py
abstracts this away into a "PageIterator" that you can use to loop over your data.

As an example, the `Client.user_search()` function takes in a keyword (like "builderman") and returns a `PageIterator`
which you can loop through to get the search results.

## Looping through items
A simple `async for` can loop through the data no problem:
```python
async for user in client.user_search("builderman"):
    print(user.name)
```

## Looping through pages
If we want to instead loop through each *page*, we can use `pages()`:
```python
async for page in client.user_search("builderman").pages():
    print("Page:")
    for user in page:
        print(f"\t{user.name}")
```
The size of this page depends on the value of the `limit` argument. It can be either 10, 20, 50 or 100. Higher values
mean you'll send less requests to get the same amount of data, however these requests will usually take longer.
```python
async for page in client.user_search("builderman", limit=100).pages():
    print(f"Page with {len(page)} items:")
    for user in page:
        print(f"\t{user.name}")
```

## Flattening into a list
If we want to turn all of this data into one list, we can use `flatten()`. Be careful, as this isn't ideal for large
sets of data and may use more memory. Because we turn this iterator into a list, we can use a normal for loop now:
```python
for user in await client.user_search("boatbomber").flatten():
    print(user.name)
```
We can also store it in a variable:
```python
users = await client.user_search("boatbomber").flatten()
print(f"{len(users)} items:")
for user in users:
    print(f"\t{user.name}")
```
