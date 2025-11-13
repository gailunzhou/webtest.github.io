# setup.py
from setuptools import setup, find_packages

setup(
    name="mkdocs-512lab-plugin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["mkdocs>=1.4"],
    entry_points={
        "mkdocs.plugins": [
            "tjcu_lab = tjcu_512lab.lab_plugin:LabAuthorPlugin",
        ]
    },
)