import setuptools
import setup_info

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(**setup_info.setup_info)
