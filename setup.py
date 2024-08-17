# coding: utf-8

from setuptools import setup

setup(
    name = 'extralist',
    packages = ['extralist'],
    version = "0.1.0a1.dev0",
    license = "LGPLv3+",
    author = "João S. O. Bueno",
    author_email = "gwidion@gmail.com",
    description = "Enhanced, maybe useful, data containers and utilities implementing sequence tupes",
    keywords = "list sequence linked linkedlist tree tuple namedtuple pagedlist",
    py_modules = ['extralist'],
    url = "https://github.com/jsbueno/extralist",
    long_description = open('README.md').read(),
    install_require = [],
    extras_require = {
        "test": ['pytest', 'pytest_benchmark'],
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ]
)
