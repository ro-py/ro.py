# Pagination
Certain Roblox endpoints are paginated. This means that going through their data is kind of like flipping through the
pages of a book - you start at page 1 and then you can move forwards or backwards until you reach the start or the end.

This can be annoying when all you want is "every member in a group" or "the last 10 posts on a group wall", so ro.py
abstracts this away into an iterator that you can use to loop over your data.

As an example, the [`Client.user_search()`][roblox.client.Client.user_search] function takes in a keyword (like "builderman") and returns a [`PageIterator`][roblox.utilities.iterators.PageIterator]
which you can loop through to get the search results.

## Looping through items
A simple `async for` can loop through the data no problem:
```python
async for user in client.user_search("builderman"):
    print(user.name)
```
We can limit the amount of items returned using the `max_items` argument:
```python
async for user in client.user_search("builderman", max_items=10):
    print(user.name)
```
We can also use `.items()`:
```python
async for user in client.user_search("builderman").items(10):
    print(user.name)
```

## Looping through pages
If we want to instead loop through each *page*, we can use `.pages()`:
```python
async for page in client.user_search("builderman").pages():
    print("Page:")
    for user in page:
        print(f"\t{user.name}")
```
The size of this page depends on the value of the `page_size` argument. It can be either 10, 25, 50 or 100. 
Higher values mean you send less requests to get the same amount of data, however these requests will usually take 
longer.

```python
async for page in client.user_search("builderman", page_size=100).pages():
    print(f"Page with {len(page)} items:")
    for user in page:
        print(f"\t{user.name}")
```

## Flattening into a list
If we want to turn all of this data into one list, we can use [`flatten()`][roblox.utilities.iterators.PageIterator.flatten]. Be careful, as this isn't ideal for large
sets of data and may use more memory. Because we turn this iterator into a list, we can use a normal for loop now:
```python
for user in await client.user_search("boatbomber").flatten():
    print(user.name)
```
We can limit the amount of items in this list using the `max_items` argument:
```python
for user in await client.user_search("builderman", max_items=10).flatten():
    print(user.name)
```
We can also pass the value directly to `.flatten()`:
```python
for user in await client.user_search("builderman").flatten(10):
    print(user.name)
```
As the result is just a normal list, we can store it in a variable:
```python
users = await client.user_search("builderman").flatten(10)
print(f"{len(users)} items:")
for user in users:
    print(f"\t{user.name}")
```

## But what about other things?
Iterators aren't *just* used for searching for users. There are also various other things that use this same concept,
including group wall posts. In this example, we get the first 10 posts on the "Official Group of Roblox" group:
```python
group = await client.get_group(1200769)
async for post in group.get_wall_posts(max_items=10):
    print(post)
```
If instead we want the *last* 10 posts (as in the most recent posts) we can use the `sort_order` argument:
```python
group = await client.get_group(1200769)
async for post in group.get_wall_posts(sort_order=SortOrder.Descending, max_items=10):
    print(post)
```
The `SortOrder` object can be imported like this:
```python
from roblox.utilities.iterators import SortOrder
```
