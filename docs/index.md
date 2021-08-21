# Overview

<div align="center">
    <img width="50%" src="assets/textlogo.svg">
</div>

Welcome to ro.py!
ro.py is an asynchronous, object-oriented wrapper for the Roblox web API.  

## Features
The key features are:  

- **Asynchronous**: ro.py works well with asynchronous frameworks like [FastAPI](https://fastapi.tiangolo.com/) and 
[discord.py](https://github.com/Rapptz/discord.py).  
- **Easy**: ro.py's client-based model is intuitive and easy to learn for both the beginner and expert developer. It
  abstracts away API requests and leaves you with simple objects that represent data types on the Roblox platform.
- **Flexible**: ro.py's builtin Requests object allows the user to do things that we haven't already implemented
ourselves without dealing with advanced Roblox-specific concepts.

## Installation
!!! warning
	ro.py is in the process of being completely rewritten for the v2.0 release.  
    All ro.py releases on PyPI (both the `ro-py` and `roblox` packages) are using the `v1.2.0.5` release, which is not
    compatible with the documentation found here.

To install ro.py from git, install [git-scm](https://git-scm.com/downloads) and run the following:
```
$ pip install git+git://github.com/rbx-libdev/ro.py.git
```

To install ro.py from PyPI, which is currently incompatible with this documentation, you can install with pip:
```
$ pip install roblox
```
