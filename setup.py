import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ro-py",
    version="0.1.6.5",
    author="jmkdev",
    author_email="jmk@jmksite.dev",
    description="ro.py is a Python wrapper for the Roblox web API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmk-developer/ro.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "iso8601",
        "signalrcore",
        "cachecontrol"
    ]
)
