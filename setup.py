import os
import re

import setuptools


def read(file_name, extract_version=False):
    content = open(os.path.join(os.path.dirname(__file__), file_name), encoding="utf8").read()
    if extract_version:
        return re.search(r'__version__ = "(.*?)"', content).group(1)
    return content

requirements = ["beautifulsoup4>=4.10.0","aiohttp>=3.9.5"]

import os

print(os.listdir("."))


setuptools.setup(
    name="MultiFeatures",
    packages=setuptools.find_packages(),
    version=read("MultiFeatures/__init__.py", extract_version=True),
    license="MIT",
    description="A versatile Python package with multiple features",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="S4tyendra",
    author_email="satya@devh.in",
    url="https://github.com/S4tyendra/MultiFeatures",
    keywords=["Tools", "Python", "12"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
)
