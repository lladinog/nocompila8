"""Package installer"""

from setuptools import find_packages, setup  # type: ignore

setup(
    name="nocompila8",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pytest",
    ],
)
