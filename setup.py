import os
from setuptools import setup

setup(
    name = "peach-config",
    version = "0.23",
    author = "Max Fowler",
    author_email = "mfowler.email@gmail.com",
    description = "Python package for configuring and updating PeachCloud",
    license = "BSD",
    url = "https://github.com/peachcloud/peach-config",
    packages=['peach_config'],
    include_package_data=True,
    entry_points = {
        'console_scripts' : [
            'peach-config = peach_config.setup_peach:main',
        ]
    },
    classifiers=[
        "License :: OSI Approved :: BSD License",
    ],
)