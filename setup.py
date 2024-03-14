"""
Code to Find Packages for Box Office Predictions
"""
from setuptools import setup, find_packages

setup(
    name='box_office_prediction',
    version='1.0',
    packages=find_packages(include=['box_office_prediction', 'box_office_prediction.*']),
    # You can also use 'exclude' to exclude certain directories
    # packages=find_packages(exclude=['data_raw']),
    # Other setup configurations...
)
