import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup_info = {
    "name": "ro-py",
    "version": "1.2.0.5",
    "author": "jmkdev and iranathan",
    "author_email": "jmk@jmksite.dev",
    "description": "ro.py is a Python wrapper for the Roblox web API.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/rbx-libdev/ro.py",
    "packages": setuptools.find_packages(),
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    "project_urls": {
        "Discord": "https://discord.gg/RJdW3gt9Ru",
        "Issue Tracker": "https://github.com/rbx-libdev/ro.py/issues",
        "GitHub": "https://github.com/rbx-libdev/ro.py/",
        "Examples": "https://github.com/rbx-libdev/ro.py/tree/main/examples"
    },
    "python_requires": '>=3.6',
    "install_requires": [
        "httpx",
        "iso8601",
        "lxml",
        "requests"
    ]
}
