# setup.py

from setuptools import setup, find_packages

setup(
    name="tap-search-ads",
    version="0.1.0",
    description="Singer tap for Google Search Ads 360 (v2 API)",
    author="Juan Ferrari",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only"
    ],
    py_modules=["tap_search_ads"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "singer-sdk>=0.27.0",
        "google-auth>=2.0.0",
        "google-api-python-client>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "tap-search-ads=tap_search_ads.tap:cli"
        ]
    },
)
