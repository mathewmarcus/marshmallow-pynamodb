from setuptools import setup, find_packages

setup(
    name="pyoneer",
    version="0.1.0",
    packages=find_packages(),
    description='PynamoDB integration with the marshmallow (de)serialization library',
    author='Mathew Marcus',
    author_email='mathewmarcus456@gmail.com',
    url='www.mathewmarcus.com',
    install_requires=[
        "marshmallow>=2.12.2",
        "pynamodb>=2.0.3",
    ]
)
