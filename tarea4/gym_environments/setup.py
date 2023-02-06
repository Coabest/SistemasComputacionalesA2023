import setuptools
from setuptools import setup

setup(
    name="gym_environments",
    version="2.0.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["gym==0.26.2", "numpy==1.23.5", "pygame", "box2d-py"],
)
