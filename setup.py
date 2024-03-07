import os

from setuptools import setup, find_packages


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as file:
        return file.read()


setup(
    name="redis_device_state",
    version="0.0.1",
    keywords=[
        "redis",
        "device",
        "data",
        "storage",
        "redis-data",
        "redis-storage",
        "redis-device",
        "device-data",
        "device-storage",
        "redis-device-data",
        "redis-device-storage",
    ],
    url="...",
    author="Fadi A.",
    author_email="fadich95@gmail.com",
    description="Device data storage based on Redis",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(
        include=[
            "redis_device_state",
            "redis_device_state.*",
        ]
    ),
    install_requires=[
        "redis==5.0.2",
    ],
    scripts=[
    ]
)
