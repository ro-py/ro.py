import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_info = {
    "name": "roblox",
    "version": "2.0.0",
    "author": "jmkdev",
    "author_email": "jmk@jmksite.dev",
    "description": "ro.py is a modern object-oriented asynchronous Python wrapper for the Roblox web API.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/ro-py/ro.py",
    "packages": setuptools.find_packages(),
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries"
    ],
    "project_urls": {
        "Discord": "https://discord.gg/tjRfCbDMSk",
        "Issue Tracker": "https://github.com/ro-py/ro.py/issues",
        "GitHub": "https://github.com/ro-py/ro.py/",
        "Examples": "https://github.com/ro-py/ro.py/tree/main/examples",
        "Twitter": "https://twitter.com/jmkdev"
    },
    "python_requires": '>=3.7',
    "install_requires": [
        "httpx>=0.21.0",
        "python-dateutil>=2.8.0"
    ]
}


setuptools.setup(**setup_info)
