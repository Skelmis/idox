import re

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

_version_regex = (
    r"^__version__ = ('|\")((?:[0-9]+\.)*[0-9]+(?:\.?([a-z]+)(?:\.?[0-9])?)?)\1$"
)

try:
    with open("idox/__init__.py") as stream:
        match = re.search(_version_regex, stream.read(), re.MULTILINE)
        version = match.group(2)
except FileNotFoundError:
    version = "0.0.0"


def parse_requirements_file(path):
    with open(path) as fp:
        dependencies = (d.strip() for d in fp.read().split("\n") if d.strip())
        return [d for d in dependencies if not d.startswith("#")]


setup(
    name="idox",
    version=version,
    author="Skelmis",
    author_email="skelmis.craft@gmail.com",
    description="IDOR file downloader using HTTP request files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        "Issue tracker": "https://github.com/Skelmis/idox/issues",
        "Documentation": "https://idox.rtfd.io/",
        "Homepage": "https://github.com/Skelmis/idox",
    },
    packages=find_packages(include=("idox", "idox.*")),
    install_requires=parse_requirements_file("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
