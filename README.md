<h1 align="center">
    <img src="https://raw.githubusercontent.com/rbx-libdev/ro.py/main/resources/header.png" alt="ro.py" width="400" />
    <br>
</h1>
<h4 align="center">ro.py is a powerful Python 3 wrapper for the Roblox Web API.</h4>
<p align="center">
  <a href="#information">Information</a> |
  <a href="#requirements">Requirements</a> |
  <a href="#disclaimer">Disclaimer</a> |
  <a href="#documentation">Documentation</a> |
  <a href="https://github.com/rbx-libdev/ro.py/tree/main/examples">Examples</a> |
  <a href="#credits">Credits</a> |
  <a href="https://github.com/rbx-libdev/ro.py/blob/main/LICENSE">License</a>
</p>

## Information
Welcome, and thank you for using ro.py!  
ro.py is an object oriented, asynchronous wrapper for the Roblox Web API (and other Roblox-related APIs) with many new and interesting features.  
ro.py allows you to automate much of what you would do on the Roblox website and on other Roblox-related websites.

## Requirements
- iso8601 (for parsing dates)
- signalrcore (for recieving notifications)
- ~~cachecontrol (for caching requests)~~
- requests-async (for sending requests, might be updated to a new lib soon)
- pytweening (for UI animations for the "prompts" extension, optional)
- wxPython (for the "prompts" extension, optional)
- wxasync (see above)

## Disclaimer
We are not responsible for any malicious use of this library.  
If you use this library in a way that violates the [Roblox Terms of Use](https://en.help.roblox.com/hc/en-us/articles/115004647846-Roblox-Terms-of-Use) your account may be punished.

## Documentation
You can view documentation for ro.py at [ro.py.jmksite.dev](https://ro.py.jmksite.dev/). If something's missing from docs, feel free to dive into the code and read the docstrings as most things are documented there.

## Installation
You can install ro.py from pip:
```
pip install ro-py
```
If you want the latest bleeding-edge version, clone from git:
```
pip install git+git://github.com/rbx-libdev/ro.py.git
```
Known issue: wxPython sometimes has trouble building on certain devices. I put wxPython last on the requirements so Python attempts to install it last, so you can safely ignore this error as everything else should be installed.

## Credits
[@iranathan](https://github.com/iranathan) - maintainer  
[@jmkdev](https://github.com/iranathan) - maintainer  
[@nsg-mfd](https://github.com/nsg-mfd) - helped with endpoints 
